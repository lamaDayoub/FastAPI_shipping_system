/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_submit_review } from '../models/Body_submit_review';
import type { Shipment } from '../models/Shipment';
import type { ShipmentCreate } from '../models/ShipmentCreate';
import type { ShipmentUpdate } from '../models/ShipmentUpdate';
import type { TagName } from '../models/TagName';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ShipmentService {
    /**
     * Get Shipment
     * @param id
     * @returns Shipment Successful Response
     * @throws ApiError
     */
    public static getShipment(
        id: string,
    ): CancelablePromise<Shipment> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/shipment/',
            query: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Submit Shipment
     * @param requestBody
     * @returns Shipment Successful Response
     * @throws ApiError
     */
    public static submitShipment(
        requestBody: ShipmentCreate,
    ): CancelablePromise<Shipment> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/shipment/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Shipment
     * @param id
     * @param requestBody
     * @returns Shipment Successful Response
     * @throws ApiError
     */
    public static updateShipment(
        id: string,
        requestBody: ShipmentUpdate,
    ): CancelablePromise<Shipment> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/shipment/',
            query: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Tracking
     * @param id
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getTracking(
        id: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/shipment/track',
            query: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Add Tag To Shipment
     * @param id
     * @param tagName
     * @returns Shipment Successful Response
     * @throws ApiError
     */
    public static addTagToShipment(
        id: string,
        tagName: TagName,
    ): CancelablePromise<Shipment> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/shipment/tag',
            query: {
                'id': id,
                'tag_name': tagName,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Remove Tag From Shipment
     * @param id
     * @param tagName
     * @returns Shipment Successful Response
     * @throws ApiError
     */
    public static removeTagFromShipment(
        id: string,
        tagName: TagName,
    ): CancelablePromise<Shipment> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/shipment/tag',
            query: {
                'id': id,
                'tag_name': tagName,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Cancel Shipment
     * @param id
     * @returns Shipment Successful Response
     * @throws ApiError
     */
    public static cancelShipment(
        id: string,
    ): CancelablePromise<Shipment> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/shipment/cancel',
            query: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Submit Review
     * @param token
     * @returns any Successful Response
     * @throws ApiError
     */
    public static submitReview(
        token: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/shipment/review',
            query: {
                'token': token,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Submit Review
     * @param token
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public static submitReview1(
        token: string,
        formData: Body_submit_review,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/shipment/review',
            query: {
                'token': token,
            },
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Shipments With Tag
     * @param tagName
     * @returns Shipment Successful Response
     * @throws ApiError
     */
    public static getShipmentsWithTag(
        tagName: TagName,
    ): CancelablePromise<Array<Shipment>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/shipmenttagged',
            query: {
                'tag_name': tagName,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
