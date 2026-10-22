/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_login_delivery_partner } from '../models/Body_login_delivery_partner';
import type { DeliveryPartnerCreate } from '../models/DeliveryPartnerCreate';
import type { DeliveryPartnerRead } from '../models/DeliveryPartnerRead';
import type { DeliveryPartnerUpdate } from '../models/DeliveryPartnerUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class DeliveryPartnerService {
    /**
     * Register Delivery Partner
     * @param requestBody
     * @returns DeliveryPartnerRead Successful Response
     * @throws ApiError
     */
    public static registerDeliveryPartner(
        requestBody: DeliveryPartnerCreate,
    ): CancelablePromise<DeliveryPartnerRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/partner/signup',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Login Delivery Partner
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public static loginDeliveryPartner(
        formData: Body_login_delivery_partner,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/partner/token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Logout Delivery Partner
     * @returns any Successful Response
     * @throws ApiError
     */
    public static logoutDeliveryPartner(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/partner/logout',
        });
    }
    /**
     * Update Delivery Partner
     * @param requestBody
     * @returns DeliveryPartnerRead Successful Response
     * @throws ApiError
     */
    public static updateDeliveryPartner(
        requestBody: DeliveryPartnerUpdate,
    ): CancelablePromise<DeliveryPartnerRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/partner/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Verify Partner Email
     * @param token
     * @returns any Successful Response
     * @throws ApiError
     */
    public static verifyPartnerEmail(
        token: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/partner/verify',
            query: {
                'token': token,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
