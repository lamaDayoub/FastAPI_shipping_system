/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Seller } from './Seller';
import type { ShipmentEvent } from './ShipmentEvent';
import type { TagRead } from './TagRead';
export type Shipment = {
    content: string;
    weight: number;
    destenation: number;
    id: string;
    seller: Seller;
    timeline: Array<ShipmentEvent>;
    estimated_delivery: string;
    tags: Array<TagRead>;
};

