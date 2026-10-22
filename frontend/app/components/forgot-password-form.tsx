// import { cn } from "cn"
// import { useContext } from "react"
// import { useNavigate } from "react-router"
// import { toast } from "sonner"

// import { Button } from "~/components/ui/button"
// import {
//   Card,
//   CardContent,
//   CardDescription,
//   CardHeader,
//   CardTitle,
// } from "~/components/ui/card"
// import {
//   Field,
//   FieldDescription,
//   FieldGroup,
//   FieldLabel,
//   FieldSeparator,
// } from "~/components/ui/field"
// import { Input } from "~/components/ui/input"
// import { AuthContext, type UserType } from "~/contexts/AuthContext"

// export function ForgotPasswordForm({
//   className,
//   user,
//   ...props
// }: { user: UserType } & React.ComponentProps<"div">) {
//   const { login } = useContext(AuthContext); // Call useContext at the top level of the 
//   const navigate = useNavigate()

//   async function loginUser(data: FormData) {
//     try {
//       const email = data.get("email")?.toString();
//       const password = data.get("password")?.toString();

//       if (!email || !password) {
//         return;
//       }

//       await login(user, email, password); // Await the async login call
//       navigate("/dashboard");
//       console.log("Navigation command executed!");
//       toast.success("Login successful!");

//     } catch (error) {
//       console.log("login failed", error);
//     }
//   };
//   return (
//     <div className={cn("flex flex-col gap-6", className)} {...props}>
//       <Card>
//         <CardHeader className="text-center">
//           <CardTitle className="text-xl">Reset your password</CardTitle>

//         </CardHeader>
//         <CardContent>
//           <form action={loginUser}>
//             <FieldGroup>
//               <Field>


//               </Field>

//               <Field>
//                 <FieldLabel htmlFor="email">Email</FieldLabel>
//                 <Input
//                   id="email"
//                   type="email"
//                   name="email"
//                   placeholder="m@example.com"
//                   required
//                 />
//               </Field>
//               <Field>
//                 <div className="flex items-center">
//                   <FieldLabel htmlFor="password">Password</FieldLabel>
//                   <a
//                     href="#"
//                     className="ml-auto text-sm underline-offset-4 hover:underline"
//                   >
//                     Forgot your password?
//                   </a>
//                 </div>
//                 <Input id="password" type="password" name="password" required />
//               </Field>
//               <Field>
//                 <Button type="submit">Reset Password</Button>

//               </Field>
//             </FieldGroup>
//           </form>
//         </CardContent>
//       </Card>

//     </div>
//   )
// }

import { cn } from "~/lib/utils" // Make sure this import path matches your project utils
import { toast } from "sonner"
import api from "~/lib/api"

import { Button } from "~/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "~/components/ui/card"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "~/components/ui/field"
import { Input } from "~/components/ui/input"
import type { UserType } from "~/contexts/AuthContext"

export function ForgotPasswordForm({
  className,
  user,
  ...props
}: { user: UserType } & React.ComponentProps<"div">) {

  async function sendResetLink(data: FormData) {
    try {
      const email = data.get("email")?.toString();

      if (!email) return;

      if (user === "seller") {
        // Pass the email string directly to match the API signature
        await api.seller.forgotPassword(email);
        toast.success("Password reset link sent! Please check your email.");
      } else {
        // Delivery partner reset password endpoint is not available on backend
        toast.error("Password reset is currently only available for sellers.");
      }

    } catch (error) {
      console.error("Failed to send reset link", error);
      toast.error("Failed to send reset link. Please check your credentials.");
    }
  }

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card>
        <CardHeader className="text-center">
          <CardTitle className="text-xl">Reset your password</CardTitle>
          <CardDescription>
            Enter your email address and we&apos;ll send you a link to reset your password.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form action={sendResetLink}>
            <FieldGroup>
              {/* Email Field Only */}
              <Field>
                <FieldLabel htmlFor="email">Email</FieldLabel>
                <Input
                  id="email"
                  type="email"
                  name="email"
                  placeholder="m@example.com"
                  required
                />
              </Field>

              {/* Submit Button */}
              <Field>
                <Button type="submit" className="w-full">
                  Send Reset Link
                </Button>
              </Field>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}