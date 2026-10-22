
import { API } from "./client";

const api = new API({
    baseUrl: "http://localhost:8000",
    securityWorker: (token) => {
        if (token) {
            return {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            };
        }
        return {};
    },
});

export default api;