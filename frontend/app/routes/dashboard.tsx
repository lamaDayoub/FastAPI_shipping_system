// import { useQuery } from "@tanstack/react-query"
// import { useContext } from "react"
// import { Navigate } from "react-router"
// import { AppSidebar } from "~/components/app-sidebar"
// import {
//   Breadcrumb,
//   BreadcrumbItem,
//   BreadcrumbLink,
//   BreadcrumbList,
//   BreadcrumbPage,
//   BreadcrumbSeparator,
// } from "~/components/ui/breadcrumb"
// import Loading from "~/components/ui/loading"
// import { Separator } from "~/components/ui/separator"
// import {
//   SidebarInset,
//   SidebarProvider,
//   SidebarTrigger,
// } from "~/components/ui/sidebar"
// import { AuthContext } from "~/contexts/AuthContext"
// import api from "~/lib/api"
// import type { Shipment } from "~/lib/client/models/Shipment"

// export default function DashboardPage() {

//   const { token, user } = useContext(AuthContext)
//   const { isLoading, isError, data: shipments } = useQuery<Shipment[]>({
//     queryKey: ["shipments"],
//     queryFn: async (): Promise<Shipment[]> => {
//       const data = user === "seller"
//         ? await api.seller.getSellerShipments()
//         : await api.deliveryPartner.getPartnerShipments();

//       return data as Shipment[];
//     },
//   });
//   if (isError) {
//     return (
//       <h1>Error Loading Shipments...</h1>
//     );
//   }
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
//       <AppSidebar currentRoute="Dashboard" />
//       <SidebarInset>
//         <header className="flex h-16 shrink-0 items-center gap-2 px-4">
//           <SidebarTrigger className="-ml-1" />
//           <Separator
//             orientation="vertical"
//             className="mr-2 data-vertical:h-4 data-vertical:self-auto"
//           />
//           <h2>Dashboard</h2>
//         </header>
//         <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
//           {isLoading || !data ? <Loading /> : (
//             <>
//               <div className="grid auto-rows-min gap-4 md:grid-cols-3">

//                 <NumberLabel value={100} label={"Total shipments"} />
//                 <NumberLabel value={25} label={"Placed"} />
//                 <NumberLabel value={70} label={"In transit"} />
//                 <NumberLabel value={5} label={"Delivered"} />
//               </div>
//               <div className="min-h-screen flex-1 rounded-xl bg-muted/50 md:min-h-min" />
//             </>
//           )
//           }
//         </div>
//       </SidebarInset>
//     </SidebarProvider>
//   )
// }
// function NumberLabel({ value, label }: { value: number; label: string }) {
//   return (
//     <div className="flex flex-col gap-2 rounded-xl border border-gray-200 p-4">
//       <h1 className="text-4xl font-bold">{value}</h1>
//       <p className="text-gray-500">{label}</p>
//     </div>
//   )
// }

import { useQuery } from "@tanstack/react-query"
import { useContext } from "react"
import { Navigate } from "react-router"
import { AppSidebar } from "~/components/app-sidebar"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "~/components/ui/breadcrumb"
import Loading from "~/components/ui/loading"
import { Separator } from "~/components/ui/separator"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "~/components/ui/sidebar"
import { AuthContext } from "~/contexts/AuthContext"
import api from "~/lib/api"
import type { Shipment } from "~/lib/client/models/Shipment"
import { getShipmentsCountForStatus } from "~/lib/utils"
import { ShipmentStatus } from "../lib/client/models/ShipmentStatus"
import ShipmentCard from "~/components/shipment-card"
export default function DashboardPage() {

  const { token, user } = useContext(AuthContext)

  const { isLoading, isError, data: shipments } = useQuery<Shipment[]>({
    queryKey: ["shipments"],
    queryFn: async (): Promise<Shipment[]> => {
      const data = user === "seller"
        ? await api.seller.getSellerShipments()
        : await api.deliveryPartner.getPartnerShipments();

      return data as Shipment[];
    },
    enabled: !!token,
  });

  if (isError) {
    return (
      <h1>Error Loading Shipments...</h1>
    );
  }
  if (token === undefined) {
    return <div className="flex h-screen items-center justify-center">Loading...</div>;
  }
  if (!token) {
    return <Navigate to="/login" />
  }

  return (
    <SidebarProvider
      style={
        {
          "--sidebar-width": "19rem",
        } as React.CSSProperties
      }
    >
      <AppSidebar currentRoute="Dashboard" />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator
            orientation="vertical"
            className="mr-2 data-vertical:h-4 data-vertical:self-auto"
          />
          <h2>Dashboard</h2>
        </header>
        <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
          {isLoading || !shipments ? <Loading /> : (
            <>
              <div className="grid auto-rows-min gap-4 md:grid-cols-3">

                <NumberLabel value={shipments.length} label="Total Shipments" />
                <NumberLabel value={getShipmentsCountForStatus(shipments, ShipmentStatus.PLACED)} label="Placed" />
                <NumberLabel value={getShipmentsCountForStatus(shipments, ShipmentStatus.IN_TRANSIT)} label="In Transit" />
                <NumberLabel value={getShipmentsCountForStatus(shipments, ShipmentStatus.DELIVERED)} label="Delivered" />
              </div>
              <div className="grid auto-rows-min gap-4 md:grid-cols-4">
                {
                  shipments.map((shipment) => (
                    <ShipmentCard shipment={shipment} />
                  ))
                }
              </div>
            </>
          )
          }
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}

function NumberLabel({ value, label }: { value: number; label: string }) {
  return (
    <div className="flex flex-col gap-2 rounded-xl border border-gray-200 p-4">
      <h1 className="text-4xl font-bold">{value}</h1>
      <p className="text-gray-500">{label}</p>
    </div>
  )
}