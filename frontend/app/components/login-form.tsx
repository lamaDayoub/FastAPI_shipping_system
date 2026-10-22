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
import { AuthContext, type UserType } from "~/contexts/AuthContext"

export function LoginForm({
  className,
  user,
  ...props
}: { user: UserType } & React.ComponentProps<"div">) {
  const { login } = useContext(AuthContext); // Call useContext at the top level of the 
  const navigate = useNavigate()


  async function loginUser(data: FormData) {
    const email = data.get("email")?.toString();
    const password = data.get("password")?.toString();

    if (!email || !password) return;

    const success = await login(user, email, password);

    if (success) {
      toast.success("Login successful!");
      navigate("/dashboard");
    } else {
      toast.error("Login failed. Please check your credentials.");
    }
  }
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
                  {/* <a
                    href={`/${user}/forgot-password`}
                    className="ml-auto text-sm underline-offset-4 hover:underline"
                  > */}
                  <a
                    href={user === "seller" ? `/${user}/forgot-password` : "#"}
                    onClick={(e) => {
                      if (user === "partner") {
                        e.preventDefault();
                        toast.info("Forgot password is not available for delivery partners yet.");
                      }
                    }}
                    className="ml-auto text-sm underline-offset-4 hover:underline cursor-pointer"
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

