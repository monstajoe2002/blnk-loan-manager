import { createUser } from "@/app/actions/user";
import { CreateUser } from "@/types";
import { useSearchParams } from "next/navigation";
import React from "react";
import { useFormStatus } from "react-dom";

export default function LoanProvider() {
  const { pending } = useFormStatus();
  const searchParams = useSearchParams();
  const username = searchParams.get("username") || "";
  const email = searchParams.get("email") || "";
  const password = searchParams.get("password") || "";
  const role = searchParams.get("role") || "";

  const user: CreateUser = {
    username,
    email,
    password,
    role,
  };

  return (
    <div>
      <form
        action={createUser.bind(null, user)}
        className="flex flex-col gap-4 my-6"
      >
        <div className="flex flex-col gap-2">
          <label htmlFor="loan-amount">Loan Amount</label>
          <input type="number" name="loan-amount" required />
        </div>
        <div className="flex flex-col gap-2">
          <label htmlFor="term">Term (in months)</label>
          <input type="number" name="term" required />
        </div>
        <div className="flex flex-col gap-2">
          <label htmlFor="interest-rate">Interest Rate</label>
          <input type="number" name="interest-rate" required />
        </div>

        <button type="submit" className={pending ? "opacity-50" : ""}>
          Finish
        </button>
      </form>
    </div>
  );
}
