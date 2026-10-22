/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ShipmentStatus } from './ShipmentStatus';
export type ShipmentEvent = {
    id: string;
    created_at: string;
    location: number;
    status: ShipmentStatus;
    description?: (string | null);
    shipment_id: string;
};

