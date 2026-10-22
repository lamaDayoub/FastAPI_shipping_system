/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ShipmentStatus } from './ShipmentStatus';
export type ShipmentUpdate = {
    location?: (number | null);
    status?: (ShipmentStatus | null);
    verification_code?: (string | null);
    description?: (string | null);
    estimated_delivery?: (string | null);
};

