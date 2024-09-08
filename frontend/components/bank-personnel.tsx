"use client";
import { createUser } from "@/app/actions/user";
import { CreateUser } from "@/types";
import { useSearchParams } from "next/navigation";
import React from "react";
import { useFormStatus } from "react-dom";

export default function BankPersonnel() {
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
          <label htmlFor="min-loan-amount">Minimum Loan Amount</label>
          <input type="number" name="min-loan-amount" required />
        </div>
        <div className="flex flex-col gap-2">
          <label htmlFor="max-loan-amount">Maximum Loan Amount</label>
          <input type="number" name="max-loan-amount" required />
        </div>
        <div className="flex flex-col gap-2">
          <label htmlFor="interest-rate">Interest Rate</label>
          <input type="number" name="interest-rate" required />
        </div>
        <div className="flex flex-col gap-2">
          <label htmlFor="loan-duration">Loan Duration (in months)</label>
          <input type="number" name="loan-duration" required />
        </div>
        <button type="submit" className={pending ? "opacity-50" : ""}>
          Finish
        </button>
      </form>
    </div>
  );
}
