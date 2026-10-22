

import { createContext, useEffect, useState } from "react";
import api from "~/lib/api";

type UserType = "seller" | "partner";

interface AuthContextType {
    token?: string | null;
    user?: UserType | null;
    login: (userType: UserType, email: string, password: string) => Promise<boolean>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
    login: async (_userType, _email, _password) => false,
    logout: () => { },
});

function AuthProvider({ children }: { children: React.ReactNode }) {
    const [token, setToken] = useState<string | null | undefined>(undefined);
    const [user, setUser] = useState<UserType | null | undefined>(undefined);

    useEffect(() => {
        const storedToken = localStorage.getItem("token");
        const storedUser = localStorage.getItem("user") as UserType | null;

        if (storedToken) {
            setToken(storedToken);
            api.setSecurityData(storedToken);
        } else {
            setToken(null);
        }

        if (storedUser) {
            setUser(storedUser);
        }
    }, []);

    async function login(userType: UserType, email: string, password: string): Promise<boolean> {
        try {
            const loginFn = userType === "seller"
                ? api.seller.loginSeller
                : api.deliveryPartner.loginDeliveryPartner;

            const response = await loginFn({ username: email, password: password });
            const accessToken = response.access_token || (response as any).data?.access_token;

            if (accessToken) {
                setToken(accessToken);
                setUser(userType);
                localStorage.setItem("token", accessToken);
                localStorage.setItem("user", userType);
                api.setSecurityData(accessToken);
                return true;
            }
            return false;
        } catch (error) {
            console.error("Login API error:", error);
            return false;
        }
    }

    async function logout() {
        if (token) {
            try {
                await api.seller.logoutSeller(token);
            } catch (error) {
                console.error("Failed to log out on backend:", error);
            }
        }

        setToken(null);
        setUser(undefined);
        api.setSecurityData(null);
        localStorage.removeItem("token");
        localStorage.removeItem("user");
    }

    return (
        <AuthContext.Provider value={{ token, user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export { AuthContext, AuthProvider, type AuthContextType, type UserType };