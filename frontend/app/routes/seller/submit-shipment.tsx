
import { useContext } from "react"
import { Navigate } from "react-router"
import { AppSidebar } from "~/components/app-sidebar"

import Loading from "~/components/ui/loading"
import { Separator } from "~/components/ui/separator"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "~/components/ui/sidebar"
import { AuthContext } from "~/contexts/AuthContext"
import { SubmitShipmentForm } from "~/components/submit-shipment-form"

interface UserProfile {
  name?: string;
  email?: string;
}

export default function SubmitShipmentPage() {
  const { token, user, logout } = useContext(AuthContext)
  if (token === undefined) {
    return <div className="flex h-screen items-center justify-center"><Loading /></div>;
  }


  if (!token) {
    return <Navigate to="/" replace />
  }
  if (user !== "seller") {
    return <Navigate to="/dashboard" replace />

  }

  // const { isLoading, isError, data: profile } = useQuery<UserProfile>({
  //   queryKey: ["account"],
  //   queryFn: async (): Promise<UserProfile> => {
  //     const data =
  //       user === "seller"
  //         ? await api.seller.getSellerMe()
  //         : await api.deliveryPartner.getDeliveryPartnerMe();

  //     return data as UserProfile;
  //   },
  //   enabled: !!token,
  // });





  return (
    <SidebarProvider
      style={
        {
          "--sidebar-width": "19rem",
        } as React.CSSProperties
      }
    >
      <AppSidebar currentRoute="Submit Shipment" />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator
            orientation="vertical"
            className="mr-2 data-vertical:h-4 data-vertical:self-auto"
          />
          <h2>Submit Shipment</h2>
        </header>

        <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
          <div className="flex flex-1 flex-col gap-4 p-4 pt-0 max-w-[600px]">
            <SubmitShipmentForm />
          </div>

        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}