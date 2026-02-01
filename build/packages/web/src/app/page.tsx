import { redirect } from "next/navigation";

export default function Home() {
  // Root redirects to dashboard (auth check happens in layout)
  redirect("/dashboard");
}
