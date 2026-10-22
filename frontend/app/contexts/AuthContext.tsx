import { createContext, useEffect, useState } from "react";

import { toast } from "sonner";
import api from "~/lib/api";


interface AuthContextType {
    token: string | null | undefined;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
}
const AuthContext = createContext<AuthContextType>({
    token: null,
    login: async () => { },
    logout: () => { },
});

function AuthProvider({ children }: { children: React.ReactNode }) {
    const [token, setToken] = useState<string | null | undefined>(undefined);

    useEffect(() => {
        const token = localStorage.getItem("token")
        if (token) {
            setToken(token)
            api.setSecurityData(token)
        }
        else {
            setToken(null)
        }
    }, [])
    async function login(email: string, password: string) {
        try {
            // Try passing username/password directly at the root level if formData caused a 422
            const response = await api.seller.loginSeller({
                username: email,
                password: password,
            });

            const accessToken = response.access_token || (response as any).data?.access_token;

            if (accessToken) {
                setToken(accessToken);
                api.setSecurityData(accessToken);
                localStorage.setItem("token", accessToken);

            }
        } catch (error) {
            toast.error("Login failed. Please check your credentials.");
        }
    }
    async function logout() {
        if (token) {
            try {
                await api.seller.logoutSeller(token); // Await backend token blacklisting
            } catch (error) {
                console.error("Failed to log out on backend:", error);
            }
        }

        // Clear local state & security headers
        setToken(null);
        api.setSecurityData(null);
        localStorage.removeItem("token"); // Clean up stored token if you're persisting it
    }
    return (
        <AuthContext.Provider value={{ token, login, logout }}>
            {children}

        </AuthContext.Provider>
    );
}
export { AuthContext, AuthProvider, type AuthContextType };

