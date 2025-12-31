import React, { useEffect, useRef, useState, useMemo } from 'react';
import * as d3 from 'd3';
import { EntityData } from '../types';

interface EntityDiagramProps {
  data: EntityData;
  scale: number;
  strokeColor: string;
  entityFillColor: string;
}

// Simple hash function for deterministic randomness
const simpleHash = (str: string) => {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return hash;
};

const EntityDiagram: React.FC<EntityDiagramProps> = ({ data, scale, strokeColor, entityFillColor }) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });
  
  // Store manually dragged positions to keep them "fixed"
  const nodePositions = useRef<{ [key: string]: { x: number, y: number } }>({});

  // Handle Resize
  useEffect(() => {
    const handleResize = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.clientWidth,
          height: containerRef.current.clientHeight,
        });
      }
    };
    
    window.addEventListener('resize', handleResize);
    handleResize(); // Initial call
    
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Calculate Layout Positions (Memoized)
  const layout = useMemo(() => {
    const { width, height } = dimensions;
    const defaultCenterX = width / 2;
    const defaultCenterY = height / 2;
    
    // Check if center is fixed
    const centerPos = nodePositions.current['__CENTER__'] || { x: defaultCenterX, y: defaultCenterY };

    // Scale distances based on the scale prop to prevent overlap when items are large
    const s = scale; 
    const baseDistanceY = 120 * s; 
    const baseDistanceX = 180 * s; 
    const topSpan = 180 * s;
    const bottomSpan = 140 * s;
    
    const attributes = data.attributes;
    const topIndices: number[] = [];
    const leftIndices: number[] = [];
    const rightIndices: number[] = [];
    const bottomIndices: number[] = [];

    // Categorize indices based on the requested logic
    attributes.forEach((_, i) => {
      if (i < 2) topIndices.push(i);
      else if (i === 2) leftIndices.push(i);
      else if (i === 3) rightIndices.push(i);
      else bottomIndices.push(i);
    });

    const attributeNodes = attributes.map((attr, i) => {
      // If manually moved, return that position immediately
      if (nodePositions.current[attr.id]) {
        return { 
            text: attr.name, 
            id: attr.id, 
            isPrimaryKey: attr.isPrimaryKey, 
            ...nodePositions.current[attr.id] 
        };
      }

      const hash = simpleHash(attr.name + i);
      const randX = (hash % 30) * s; 
      const randY = ((hash >> 5) % 30) * s;
      const randLen = ((hash >> 3) % 40) * s;

      let x = defaultCenterX;
      let y = defaultCenterY;

      if (topIndices.includes(i)) {
         const count = topIndices.length;
         const indexInZone = topIndices.indexOf(i);
         const startX = defaultCenterX - ((count - 1) * topSpan) / 2;
         x = startX + indexInZone * topSpan + randX;
         y = defaultCenterY - baseDistanceY - randLen;
      } else if (leftIndices.includes(i)) {
         x = defaultCenterX - baseDistanceX - randLen;
         y = defaultCenterY + randY;
      } else if (rightIndices.includes(i)) {
         x = defaultCenterX + baseDistanceX + randLen;
         y = defaultCenterY + randY;
      } else {
         const count = bottomIndices.length;
         const indexInZone = bottomIndices.indexOf(i);
         const rowWidth = (count - 1) * bottomSpan;
         const startX = defaultCenterX - rowWidth / 2;
         x = startX + indexInZone * bottomSpan + randX;
         y = defaultCenterY + baseDistanceY + randLen;
         if (count > 3) {
             y += (indexInZone % 2 === 0 ? 0 : 40 * s);
         }
      }

      return { text: attr.name, id: attr.id, isPrimaryKey: attr.isPrimaryKey, x, y };
    });

    return { center: { ...centerPos, id: '__CENTER__', text: data.name }, attributes: attributeNodes };
  }, [data.attributes, data.name, dimensions, scale]);

  // D3 Rendering & Drag Logic
  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove(); 

    // Scaled dimensions
    const rectWidth = 140 * scale;
    const rectHeight = 60 * scale;
    const ellipseRx = 70 * scale;
    const ellipseRy = 40 * scale;
    const fontSizeCenter = 18 * scale;
    const fontSizeAttr = 14 * scale;
    const strokeWidth = 2 * Math.sqrt(scale); // Scale stroke slightly less aggressively

    // --- Drag Behavior ---
    const drag = d3.drag<SVGGElement, any>()
      .on("start", function(event, d) {
        d3.select(this).attr("cursor", "grabbing");
        d3.select(this).raise(); 
      })
      .on("drag", function(event, d) {
        d.x = event.x;
        d.y = event.y;

        d3.select(this).attr("transform", `translate(${d.x},${d.y})`);

        if (d.id === '__CENTER__') {
          svg.selectAll(".link-line")
            .attr("x1", d.x)
            .attr("y1", d.y);
        } else {
          svg.selectAll<SVGLineElement, any>(".link-line")
             .filter(lineData => lineData.targetId === d.id)
             .attr("x2", d.x)
             .attr("y2", d.y);
        }

        nodePositions.current[d.id] = { x: d.x, y: d.y };
      })
      .on("end", function(event, d) {
        d3.select(this).attr("cursor", "grab");
      });

    // 1. Draw Links (Lines)
    const linkData = layout.attributes.map(attr => ({
        targetId: attr.id,
        x1: layout.center.x,
        y1: layout.center.y,
        x2: attr.x,
        y2: attr.y
    }));

    svg.selectAll(".link-line")
       .data(linkData)
       .enter()
       .append("line")
       .attr("class", "link-line")
       .attr("x1", d => d.x1)
       .attr("y1", d => d.y1)
       .attr("x2", d => d.x2)
       .attr("y2", d => d.y2)
       .attr("stroke", strokeColor) 
       .attr("stroke-width", strokeWidth);

    // 2. Draw Center Entity
    const centerGroup = svg.append("g")
      .data([layout.center])
      .attr("transform", d => `translate(${d.x}, ${d.y})`)
      .attr("cursor", "grab")
      .call(drag);

    centerGroup.append("rect")
      .attr("x", -rectWidth / 2)
      .attr("y", -rectHeight / 2)
      .attr("width", rectWidth)
      .attr("height", rectHeight)
      .attr("fill", entityFillColor)
      .attr("stroke", strokeColor) 
      .attr("stroke-width", strokeWidth + 0.5)
      .attr("rx", 4 * scale);

    centerGroup.append("text")
      .text(d => d.text)
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "middle")
      .style("font-family", "inherit")
      .style("font-weight", "bold")
      .style("font-size", `${fontSizeCenter}px`)
      .style("fill", "#111827") // gray-900
      .style("pointer-events", "none");

    // 3. Draw Attributes
    const attributeGroups = svg.selectAll(".attr-group")
      .data(layout.attributes)
      .enter()
      .append("g")
      .attr("class", "attr-group")
      .attr("transform", d => `translate(${d.x}, ${d.y})`)
      .attr("cursor", "grab")
      .call(drag);

    attributeGroups.append("ellipse")
      .attr("cx", 0)
      .attr("cy", 0)
      .attr("rx", ellipseRx)
      .attr("ry", ellipseRy)
      .attr("fill", "white")
      .attr("stroke", strokeColor) 
      .attr("stroke-width", strokeWidth);

    attributeGroups.each(function(d) {
      const g = d3.select(this);
      const textElement = g.append("text")
        .attr("text-anchor", "middle")
        .attr("dominant-baseline", "middle")
        .style("font-family", "inherit")
        .style("font-weight", "500")
        .style("font-size", `${fontSizeAttr}px`)
        .style("fill", "#374151") // gray-700
        .style("pointer-events", "none");

      if (d.isPrimaryKey) {
        textElement.style("text-decoration", "underline");
        textElement.style("font-weight", "bold");
      }

      // Simple text wrapping for scalable text
      if (d.text.length > 12) {
         const words = d.text.split(' ');
         if (words.length > 1) {
             const dy = fontSizeAttr * 1.2;
             textElement.append("tspan").text(words.slice(0, Math.ceil(words.length/2)).join(' ')).attr("x", 0).attr("dy", -dy * 0.3);
             textElement.append("tspan").text(words.slice(Math.ceil(words.length/2)).join(' ')).attr("x", 0).attr("dy", dy);
         } else {
             textElement.text(d.text);
         }
      } else {
          textElement.text(d.text);
      }
    });

  }, [layout, dimensions, scale, strokeColor, entityFillColor]);

  return (
    <div ref={containerRef} className="w-full h-full min-h-[500px] bg-white rounded-xl shadow-inner border border-slate-200 overflow-hidden relative">
      <svg ref={svgRef} width="100%" height="100%" viewBox={`0 0 ${dimensions.width} ${dimensions.height}`} />
      <div className="absolute bottom-4 right-4 bg-white/80 backdrop-blur-sm p-2 rounded-lg text-xs text-slate-500 border border-slate-200 pointer-events-none">
        Drag nodes to fix positions • Underlined items are Primary Keys
      </div>
    </div>
  );
};

export default EntityDiagram;