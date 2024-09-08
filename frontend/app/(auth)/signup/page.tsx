"use client";

import { Role } from "@/types";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";

export default function SignupPage() {
  const router = useRouter();
  const [role, setRole] = useState<Role>("bank-personnel");

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // pass form data to next page
    const formData = new FormData(e.target as HTMLFormElement);
    const data = Object.fromEntries(formData.entries()) as Record<
      string,
      string
    >;
    
   
    router.push(`/signup/${role}?${new URLSearchParams(data).toString()}`);
  };

  return (
    <div>
      <h1>Signup</h1>
      <form className="flex flex-col gap-4 my-6" onSubmit={handleSubmit}>
        <div className="flex flex-col gap-2">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            name="email"
            placeholder="user@blnk.com"
            required
          />
        </div>
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
        <div className="flex flex-col gap-2">
          <label htmlFor="role">Role</label>
          <select name="role" onChange={(e) => setRole(e.target.value as Role)}>
            <option value="bank-personnel">Bank Personnel</option>
            <option value="loan-customer">Loan Customer</option>
            <option value="loan-provider">Loan Provider</option>
          </select>
        </div>

        <button type="submit">Next</button>
      </form>
      <Link href="/login">Already have an account? Login</Link>
    </div>
  );
}
