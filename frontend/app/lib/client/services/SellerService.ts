/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_login_seller } from '../models/Body_login_seller';
import type { Body_reset_password } from '../models/Body_reset_password';
import type { SellerCreate } from '../models/SellerCreate';
import type { SellerRead } from '../models/SellerRead';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class SellerService {
    /**
     * Register Seller
     * @param requestBody
     * @returns SellerRead Successful Response
     * @throws ApiError
     */
    public static registerSeller(
        requestBody: SellerCreate,
    ): CancelablePromise<SellerRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/seller/signup',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Login Seller
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public static loginSeller(
        formData: Body_login_seller,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/seller/token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Logout Seller
     * @param token
     * @returns any Successful Response
     * @throws ApiError
     */
    public static logoutSeller(
        token: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/seller/logout',
            query: {
                'token': token,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Verify Seller Email
     * @param token
     * @returns any Successful Response
     * @throws ApiError
     */
    public static verifySellerEmail(
        token: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/seller/verify',
            query: {
                'token': token,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Forgot Password
     * @param email
     * @returns any Successful Response
     * @throws ApiError
     */
    public static forgotPassword(
        email: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/seller/forgot_password',
            query: {
                'email': email,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Reset Password Form
     * @param token
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getResetPasswordForm(
        token: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/seller/reset_password_form',
            query: {
                'token': token,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Reset Password
     * @param token
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public static resetPassword(
        token: string,
        formData: Body_reset_password,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/seller/reset_password',
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
     * Get Seller Me
     * @returns SellerRead Successful Response
     * @throws ApiError
     */
    public static getSellerMe(): CancelablePromise<SellerRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/seller/me',
        });
    }
}
