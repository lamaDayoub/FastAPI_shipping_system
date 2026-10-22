// app/lib/client.ts
import { OpenAPI } from "./client/core/OpenAPI";
import { SellerService } from "./client/services/SellerService";
import { ShipmentService } from "./client/services/ShipmentService";
import { DeliveryPartnerService } from "./client/services/DeliveryPartnerService";

export interface ApiConfig {
    baseUrl?: string;
    securityWorker?: (token: string | null) => { headers?: Record<string, string> } | void;
}

export class API {
    seller = SellerService;
    shipment = ShipmentService;
    deliveryPartner = DeliveryPartnerService;

    private securityWorkerFn?: (token: string | null) => { headers?: Record<string, string> } | void;

    constructor(config?: ApiConfig) {
        if (config?.baseUrl) {
            OpenAPI.BASE = config.baseUrl;
        }
        if (config?.securityWorker) {
            this.securityWorkerFn = config.securityWorker;
        }
    }

    setSecurityData(token: string | null) {
        // 1. Direct built-in support for openapi-typescript-codegen token handling
        OpenAPI.TOKEN = token ?? undefined;

        // 2. Call securityWorker callback if provided
        if (this.securityWorkerFn) {
            this.securityWorkerFn(token);
        }
    }
}