
import React, { useState, useCallback, useMemo } from 'react';
import { Plus, Trash2, Wand2, Download, AlertCircle, Key, Settings2 } from 'lucide-react';
import EntityDiagram from './components/EntityDiagram';
import { generateAttributes } from './services/geminiService';
import { EntityData, Attribute } from './types';

// Helper to generate IDs
const generateId = () => Math.random().toString(36).substring(2, 9);

const App: React.FC = () => {
  const [entityName, setEntityName] = useState<string>('Pet');
  
  // Initialize with objects
  const [attributes, setAttributes] = useState<Attribute[]>([
    { id: '1', name: 'Pet ID', isPrimaryKey: true },
    { id: '2', name: 'Name', isPrimaryKey: false },
    { id: '3', name: 'Age', isPrimaryKey: false },
    { id: '4', name: 'Owner ID', isPrimaryKey: false },
    { id: '5', name: 'Breed', isPrimaryKey: false }
  ]);

  // Appearance State
  const [scale, setScale] = useState<number>(1);
  const [strokeColor, setStrokeColor] = useState<string>('#4b5563'); // gray-600
  const [entityFillColor, setEntityFillColor] = useState<string>('#ffffff');
  
  const [newAttribute, setNewAttribute] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleAddAttribute = useCallback(() => {
    if (newAttribute.trim()) {
      setAttributes((prev) => [
        ...prev, 
        { id: generateId(), name: newAttribute.trim(), isPrimaryKey: false }
      ]);
      setNewAttribute('');
    }
  }, [newAttribute]);

  const handleRemoveAttribute = useCallback((id: string) => {
    setAttributes((prev) => prev.filter((attr) => attr.id !== id));
  }, []);

  const handleTogglePrimaryKey = useCallback((id: string) => {
    setAttributes((prev) => prev.map(attr => 
      attr.id === id ? { ...attr, isPrimaryKey: !attr.isPrimaryKey } : attr
    ));
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleAddAttribute();
    }
  };

  const handleGeminiGenerate = async () => {
    if (!entityName.trim()) {
        setError("Please enter an Entity Name first.");
        return;
    }
    setError(null);
    setIsLoading(true);
    try {
      const generatedStrings = await generateAttributes(entityName);
      if (generatedStrings.length > 0) {
        // Convert strings to Attribute objects
        const newAttributes: Attribute[] = generatedStrings.map(name => ({
            id: generateId(),
            name: name,
            isPrimaryKey: name.toLowerCase().includes('id') && name.toLowerCase().includes(entityName.toLowerCase()) // Simple heuristic
        }));
        
        // Smart guess PK if not set
        let pkFound = false;
        newAttributes.forEach(attr => {
            if (!pkFound && (attr.name.toLowerCase() === 'id' || attr.name.toLowerCase() === `${entityName.toLowerCase()}id` || attr.name.toLowerCase() === `${entityName.toLowerCase()}_id`)) {
                attr.isPrimaryKey = true;
                pkFound = true;
            } else {
                attr.isPrimaryKey = false;
            }
        });

        setAttributes(newAttributes);
      } else {
        setError("AI could not generate attributes. Please check your API key or try again.");
      }
    } catch (e) {
      setError("An unexpected error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  const downloadSvg = () => {
    const svgElement = document.querySelector('svg');
    if (!svgElement) return;

    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(svgElement);
    const blob = new Blob([source], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `${entityName.toLowerCase()}_er_diagram.svg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const diagramData: EntityData = useMemo(() => ({
    name: entityName,
    attributes: attributes,
  }), [entityName, attributes]);

  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-slate-50 text-slate-800 font-sans">
      {/* Sidebar Controls */}
      <div className="w-full md:w-96 bg-white border-r border-slate-200 p-6 flex flex-col h-auto md:h-screen overflow-y-auto shadow-lg z-10">
        <header className="mb-6">
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
            <span className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white text-sm">ER</span>
            Entity Graph
          </h1>
          <p className="text-sm text-slate-500 mt-2">Generate ER diagrams automatically.</p>
        </header>

        <div className="space-y-6 flex-1">
          {/* Entity Name Input */}
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">
              Entity Name (Center)
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={entityName}
                onChange={(e) => setEntityName(e.target.value)}
                className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                placeholder="e.g. User, Order, Product"
              />
            </div>
          </div>

          {/* AI Generator Button */}
           <div className="p-4 bg-indigo-50 rounded-xl border border-indigo-100">
            <div className="flex items-start gap-3">
               <Wand2 className="w-5 h-5 text-indigo-600 mt-0.5" />
               <div>
                 <h3 className="text-sm font-semibold text-indigo-900">AI Auto-Fill</h3>
                 <p className="text-xs text-indigo-700 mt-1 mb-3">
                   Generate attributes automatically using Gemini AI.
                 </p>
                 <button
                  onClick={handleGeminiGenerate}
                  disabled={isLoading}
                  className="w-full py-2 px-4 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white rounded-lg text-sm font-medium transition flex items-center justify-center gap-2"
                >
                  {isLoading ? 'Generating...' : 'Generate Attributes'}
                </button>
               </div>
            </div>
            {error && (
                <div className="mt-3 text-xs text-red-600 flex items-center gap-1">
                    <AlertCircle className="w-3 h-3" /> {error}
                </div>
            )}
          </div>

          <div className="border-t border-slate-100 my-2"></div>

          {/* Appearance Section */}
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
            <h3 className="text-sm font-semibold text-slate-900 flex items-center gap-2 mb-3">
                <Settings2 size={16} /> Appearance
            </h3>
            
            <div className="space-y-4">
                <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1 flex justify-between">
                        <span>Size / Zoom</span>
                        <span>{Math.round(scale * 100)}%</span>
                    </label>
                    <input 
                        type="range" 
                        min="0.5" 
                        max="1.5" 
                        step="0.1" 
                        value={scale}
                        onChange={(e) => setScale(parseFloat(e.target.value))}
                        className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                    />
                </div>

                <div className="flex gap-4">
                    <div className="flex-1">
                        <label className="block text-xs font-medium text-slate-600 mb-1">Stroke Color</label>
                        <div className="flex items-center gap-2">
                            <input 
                                type="color" 
                                value={strokeColor}
                                onChange={(e) => setStrokeColor(e.target.value)}
                                className="h-8 w-8 rounded cursor-pointer border-0 p-0"
                            />
                            <span className="text-xs text-slate-500 font-mono">{strokeColor}</span>
                        </div>
                    </div>
                     <div className="flex-1">
                        <label className="block text-xs font-medium text-slate-600 mb-1">Entity Fill</label>
                        <div className="flex items-center gap-2">
                            <input 
                                type="color" 
                                value={entityFillColor}
                                onChange={(e) => setEntityFillColor(e.target.value)}
                                className="h-8 w-8 rounded cursor-pointer border-0 p-0"
                            />
                            <span className="text-xs text-slate-500 font-mono">{entityFillColor}</span>
                        </div>
                    </div>
                </div>
            </div>
          </div>

          <div className="border-t border-slate-100 my-2"></div>

          {/* Attributes List */}
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">
              Attributes ({attributes.length})
            </label>
            
            <div className="flex gap-2 mb-3">
              <input
                type="text"
                value={newAttribute}
                onChange={(e) => setNewAttribute(e.target.value)}
                onKeyDown={handleKeyDown}
                className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none text-sm"
                placeholder="Add attribute..."
              />
              <button
                onClick={handleAddAttribute}
                className="p-2 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition"
                aria-label="Add Attribute"
              >
                <Plus size={20} />
              </button>
            </div>

            <ul className="space-y-2 max-h-[300px] overflow-y-auto pr-1">
              {attributes.map((attr) => (
                <li key={attr.id} className="group flex items-center justify-between p-2 bg-slate-50 border border-slate-200 rounded-md hover:border-indigo-300 transition">
                  <div className="flex items-center gap-2 overflow-hidden">
                      <button 
                        onClick={() => handleTogglePrimaryKey(attr.id)}
                        className={`p-1 rounded-md transition ${attr.isPrimaryKey ? 'bg-amber-100 text-amber-600' : 'text-slate-300 hover:text-slate-500'}`}
                        title="Toggle Primary Key"
                      >
                         <Key size={14} className={attr.isPrimaryKey ? 'fill-current' : ''} />
                      </button>
                      <span className={`text-sm truncate ${attr.isPrimaryKey ? 'font-semibold text-indigo-900 underline decoration-indigo-300' : 'text-slate-700'}`}>
                        {attr.name}
                      </span>
                  </div>
                  <button
                    onClick={() => handleRemoveAttribute(attr.id)}
                    className="text-slate-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition ml-2"
                    title="Remove"
                  >
                    <Trash2 size={16} />
                  </button>
                </li>
              ))}
              {attributes.length === 0 && (
                <li className="text-center text-sm text-slate-400 py-4 italic">
                  No attributes added yet.
                </li>
              )}
            </ul>
          </div>
        </div>
        
        <div className="mt-auto pt-6 border-t border-slate-200">
             <button 
                onClick={downloadSvg}
                className="w-full flex items-center justify-center gap-2 py-2.5 border border-slate-300 rounded-lg text-slate-600 text-sm font-medium hover:bg-slate-50 transition"
             >
                <Download size={16} /> Export SVG
             </button>
        </div>
      </div>

      {/* Main Canvas Area */}
      <main className="flex-1 bg-slate-100 p-4 md:p-8 flex flex-col h-[50vh] md:h-screen">
        <div className="flex-1 relative">
             <EntityDiagram 
                data={diagramData} 
                scale={scale} 
                strokeColor={strokeColor} 
                entityFillColor={entityFillColor}
             />
        </div>
      </main>
    </div>
  );
};

export default App;
