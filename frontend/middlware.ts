import type { NextRequest } from "next/server";
import { getLoggedInUser } from "./app/data/user";
import { NextResponse } from "next/server";
export async function middleware(req: NextRequest) {
  const user = await getLoggedInUser();
  if (!user && req.nextUrl.pathname !== "/login") {
    return NextResponse.redirect(new URL("/login", req.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: "/",
};
