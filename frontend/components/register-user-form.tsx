"use client";
import { Role } from "@/types";
import React from "react";
import BankPersonnel from "@/components/bank-personnel";
import LoanCustomer from "./loan-customer";
import LoanProvider from "./loan-provider";

type Props = {
  role: Role;
};

export default function RegisterUserForm({ role }: Props) {
  switch (role) {
    case "bank-personnel":
      return <BankPersonnel />;
    case "loan-customer":
      return <LoanCustomer />;
    case "loan-provider":
      return <LoanProvider />;
    default:
      return (
        <div className="text-red-500 flex my-8 text-lg">
          <span>Invalid role</span>
        </div>
      );
  }
}
