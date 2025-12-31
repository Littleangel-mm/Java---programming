export interface Attribute {
  id: string;
  name: string;
  isPrimaryKey: boolean;
}

export interface EntityData {
  name: string;
  attributes: Attribute[];
}

export enum DiagramType {
  STAR = 'STAR',
}
