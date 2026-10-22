import { cn } from "cn"
import { useContext } from "react"
import { useNavigate } from "react-router"
import { toast } from "sonner"

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
  FieldSeparator,
} from "~/components/ui/field"
import { Input } from "~/components/ui/input"
import { AuthContext } from "~/contexts/AuthContext"

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"div">) {
  const { login } = useContext(AuthContext); // Call useContext at the top level of the 
  const navigate = useNavigate()

  async function loginUser(data: FormData) {
    try {
      const email = data.get("email")?.toString();
      const password = data.get("password")?.toString();

      if (!email || !password) {
        return;
      }

      await login(email, password); // Await the async login call
      navigate("/dashboard");
      console.log("Navigation command executed!");
      toast.success("Login successful!");

    } catch (error) {
      console.log("login failed", error);
    }
  };
  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card>
        <CardHeader className="text-center">
          <CardTitle className="text-xl">Welcome back</CardTitle>

        </CardHeader>
        <CardContent>
          <form action={loginUser}>
            <FieldGroup>
              <Field>


              </Field>

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
              <Field>
                <div className="flex items-center">
                  <FieldLabel htmlFor="password">Password</FieldLabel>
                  <a
                    href="#"
                    className="ml-auto text-sm underline-offset-4 hover:underline"
                  >
                    Forgot your password?
                  </a>
                </div>
                <Input id="password" type="password" name="password" required />
              </Field>
              <Field>
                <Button type="submit">Login</Button>
                <FieldDescription className="text-center">
                  Don&apos;t have an account? <a href="#">Sign up</a>
                </FieldDescription>
              </Field>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>

    </div>
  )
}

// import { cn } from "~/lib/utils" // Note: updated 'cn' import to point to your utils
// import { Button } from "~/components/ui/button"
// import {
//   Card,
//   CardContent,
//   CardHeader,
//   CardTitle,
// } from "~/components/ui/card"
// import {
//   Field,
//   FieldDescription,
//   FieldGroup,
//   FieldLabel,
// } from "~/components/ui/field"
// import { Input } from "~/components/ui/input"
// import { useContext } from "react"
// import { AuthContext } from "~/contexts/AuthContext"

// // Add props so the parent component (Login route) can pass the onSubmit handler
// interface LoginFormProps extends React.ComponentProps<"div"> {
//   onSubmit?: (email: string, password: string) => void;
// }

// export function LoginForm({
//   className,
//   onSubmit,
//   ...props
// }: LoginFormProps) {

//   function loginUser(data: FormData) {
//     try {
//       const { login } = useContext(AuthContext);
//       const email = data.get("email")?.toString();
//       const password = data.get("password")?.toString();

//       if (!email || !password) {
//         return
//       }
//       login(email, password)

//     } catch (error) {
//       console.log("login failed")
//     }

//   };

//   return (
//     <div className={cn("flex flex-col gap-6", className)} {...props}>
//       <Card>
//         <CardHeader className="text-center">
//           <CardTitle className="text-xl">Welcome back</CardTitle>
//         </CardHeader>
//         <CardContent>
//           <form action={loginUser}>
//             <FieldGroup>
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
//                 <Button type="submit" className="w-full">Login</Button>
//                 <FieldDescription className="text-center mt-2">
//                   Don&apos;t have an account? <a href="#" className="underline">Sign up</a>
//                 </FieldDescription>
//               </Field>
//             </FieldGroup>
//           </form>
//         </CardContent>
//       </Card>
//     </div>
//   )
// }