// import type { Route } from "./+types/home";
// import { Welcome } from "../welcome/welcome";
// import { Button } from "~/components/ui/button";
// import { Link } from "react-router";

// export function meta({ }: Route.MetaArgs) {
//   return [
//     { title: "New React Router App" },
//     { name: "description", content: "Welcome to React Router!" },
//   ];
// }

// export default function Home() {
//   return (
//     <div>
//       <Button>Welcome </Button>
//       <Button asChild>
//         <Link to="seller/login">Seller Login</Link>
//       </Button>
//       <Button asChild>
//         <Link to="partner/login">Partner Login</Link>
//       </Button>


//     </div>
//   )
// }
import type { Route } from "./+types/home";
import { Button } from "~/components/ui/button";
import { Link } from "react-router";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Logistics Portal - Home" },
    { name: "description", content: "Welcome to the Logistics Management Portal" },
  ];
}

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-slate-50 p-6">
      <div className="w-full max-w-md bg-white rounded-xl shadow-lg border border-slate-100 p-8 text-center space-y-6">

        {/* Welcome Header */}
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            Welcome Portal
          </h1>
          <p className="text-sm text-slate-500">
            Select your account type below to log in to your portal.
          </p>
        </div>

        {/* Navigation Buttons */}
        <div className="flex flex-col gap-3 pt-2">
          <Button asChild size="lg" className="w-full font-medium">
            <Link to="/seller/login">Seller Login</Link>
          </Button>

          <Button asChild variant="outline" size="lg" className="w-full font-medium">
            <Link to="/partner/login">Delivery Partner Login</Link>
          </Button>
        </div>

      </div>
    </main>
  );
}