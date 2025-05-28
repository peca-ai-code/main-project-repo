import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "PECA - Your Reproductive Health Partner | AI-Powered Women's Healthcare",
  description:
    "Connect with certified gynecologists, get AI-powered health insights, and take control of your reproductive wellness journey with PECA. Trusted by 50,000+ women worldwide.",
  keywords: "reproductive health, gynecologist, women's health, AI health assistant, telemedicine, healthcare platform",
  authors: [{ name: "PECA Health" }],
  creator: "PECA Health",
  publisher: "PECA Health",
  robots: "index, follow",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://peca.health",
    title: "PECA - Your Reproductive Health Partner",
    description: "AI-powered reproductive health platform connecting women with expert gynecologists",
    siteName: "PECA Health",
  },
  twitter: {
    card: "summary_large_image",
    title: "PECA - Your Reproductive Health Partner",
    description: "AI-powered reproductive health platform connecting women with expert gynecologists",
    creator: "@pecahealth",
  },
  viewport: "width=device-width, initial-scale=1",
  themeColor: "#EC4899",
    generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <meta name="theme-color" content="#EC4899" />
      </head>
      <body className={inter.className}>{children}</body>
    </html>
  )
}
