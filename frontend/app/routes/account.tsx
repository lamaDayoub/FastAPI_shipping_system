// import { useQuery } from "@tanstack/react-query"
// import { useContext } from "react"
// import { Navigate } from "react-router"
// import { AppSidebar } from "~/components/app-sidebar"
// import { Button } from "~/components/ui/button"
// import { Input } from "~/components/ui/input"
// import { Label } from "~/components/ui/label"
// import Loading from "~/components/ui/loading"
// import { Separator } from "~/components/ui/separator"
// import {
//   SidebarInset,
//   SidebarProvider,
//   SidebarTrigger,
// } from "~/components/ui/sidebar"
// import { AuthContext } from "~/contexts/AuthContext"
// import api from "~/lib/api"
// interface UserProfile {
//   name?: string;
//   email?: string;
// }
// export default function AccountPage() {

//   const { token, user, logout } = useContext(AuthContext)

//   const { isLoading, isError, data: profile } = useQuery<UserProfile>({
//     queryKey: ["account"],
//     queryFn: async (): Promise<UserProfile> => {
//       const data =
//         user === "seller"
//           ? await api.seller.getSellerMe()
//           : await api.deliveryPartner.getDeliveryPartnerMe();

//       return data as UserProfile;
//     },
//     enabled: !!token,
//   });
//   if (isLoading) return <div>Loading profile...</div>;
//   if (isError) return <div>Failed to load account details.</div>;

//   if (token === undefined) {
//     return <div className="flex h-screen items-center justify-center">Loading...</div>;
//   }
//   if (!token) {
//     return <Navigate to="/login" />
//   }

//   return (
//     <SidebarProvider
//       style={
//         {
//           "--sidebar-width": "19rem",
//         } as React.CSSProperties
//       }
//     >
//       <AppSidebar currentRoute="Account" />
//       <SidebarInset>
//         <header className="flex h-16 shrink-0 items-center gap-2 px-4">
//           <SidebarTrigger className="-ml-1" />
//           <Separator
//             orientation="vertical"
//             className="mr-2 data-vertical:h-4 data-vertical:self-auto"
//           />
//           <h2>Account</h2>
//         </header>
//         <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
//           {isLoading || !profile ? <Loading /> :
//             (
//               <div className="flex flex-col gap-4 max-w-[400px]">
//                 <Label htmlFor="name">Name</Label>
//                 <Input id="name" value={profile?.name ?? "..."} readOnly />
//                 <Label htmlFor="email">Email</Label>
//                 <Input id="email" value={profile?.email ?? "..."} readOnly />
//                 <Button className="w-min ml-auto" onClick={logout}>Log Out</Button>
//               </div>

//             )
//           }
//         </div>
//       </SidebarInset>
//     </SidebarProvider>
//   )
// }

import { useQuery } from "@tanstack/react-query"
import { useContext } from "react"
import { Navigate } from "react-router"
import { AppSidebar } from "~/components/app-sidebar"
import { Button } from "~/components/ui/button"
import { Input } from "~/components/ui/input"
import { Label } from "~/components/ui/label"
import Loading from "~/components/ui/loading"
import { Separator } from "~/components/ui/separator"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "~/components/ui/sidebar"
import { AuthContext } from "~/contexts/AuthContext"
import api from "~/lib/api"

interface UserProfile {
  name?: string;
  email?: string;
}

export default function AccountPage() {
  const { token, user, logout } = useContext(AuthContext)

  const { isLoading, isError, data: profile } = useQuery<UserProfile>({
    queryKey: ["account"],
    queryFn: async (): Promise<UserProfile> => {
      const data =
        user === "seller"
          ? await api.seller.getSellerMe()
          : await api.deliveryPartner.getDeliveryPartnerMe();

      return data as UserProfile;
    },
    enabled: !!token,
  });

  // 1. Auth check: Wait for auth context to load
  if (token === undefined) {
    return <div className="flex h-screen items-center justify-center"><Loading /></div>;
  }

  // 2. Auth check: Redirect unauthenticated users to home ("/") per course script
  if (!token) {
    return <Navigate to="/" replace />
  }

  return (
    <SidebarProvider
      style={
        {
          "--sidebar-width": "19rem",
        } as React.CSSProperties
      }
    >
      <AppSidebar currentRoute="Account" />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator
            orientation="vertical"
            className="mr-2 data-vertical:h-4 data-vertical:self-auto"
          />
          <h2>Account</h2>
        </header>

        <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
          {isLoading || !profile ? (
            <Loading />
          ) : isError ? (
            <div>Failed to load account details.</div>
          ) : (
            <div className="flex flex-col gap-4 max-w-[400px]">
              <div className="space-y-2">
                <Label htmlFor="name">Name</Label>
                <Input id="name" value={profile?.name ?? "..."} readOnly />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input id="email" value={profile?.email ?? "..."} readOnly />
              </div>

              <Button className="w-min ml-auto" onClick={logout}>
                Log Out
              </Button>
            </div>
          )}
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}