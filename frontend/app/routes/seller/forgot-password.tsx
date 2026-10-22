"use client"


import { GalleryVerticalEndIcon } from "lucide-react"
import { ForgotPasswordForm } from "~/components/forgot-password-form"

export default function SellerForgotPasswordPage() {
    return (
        <div className="flex min-h-svh flex-col items-center justify-center gap-6 bg-muted p-6 md:p-10">
            <div className="flex w-full max-w-sm flex-col gap-6">
                <h1 className=" text-5xl flex items-center gap-2 self-center font-medium">

                    FastShip
                </h1>
                <ForgotPasswordForm user="seller" />
            </div>
        </div>
    )
}
