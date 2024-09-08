import { login } from "@/app/actions/user";
import Link from "next/link";
export default function LoginPage() {
  return (
    <div>
      <h1>Login</h1>

      <form action={login} className="flex flex-col gap-4 my-6">
        <div className="flex flex-col gap-2">
          <label htmlFor="username">Username</label>
          <input type="text" name="username" placeholder="user_blnk" required />
        </div>
        <div className="flex flex-col gap-2">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            name="password"
            placeholder="********"
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
      <Link href="/signup">Don&apos;t have an account? Signup</Link>
    </div>
  );
}
