"use server";

import { BankPersonnel, CreateUser, LoanCustomer, LoanProvider } from "@/types";
import { getAllUsers, registerUser } from "../data/user";
import { cookies } from "next/headers";
import { redirect, RedirectType } from "next/navigation";
export async function createUser(user: CreateUser, formData: FormData) {
  const personnel_minLoanAmount = Number(formData.get("min-loan-amount"));
  const personnel_maxLoanAmount = Number(formData.get("max-loan-amount"));
  const personnel_interestRate = Number(formData.get("interest-rate"));
  const personnel_loanDuration = Number(formData.get("loan-duration"));
  const customer_amount = Number(formData.get("amount"));
  const customer_term = Number(formData.get("term"));
  const customer_interestRate = Number(formData.get("interest-rate"));
  const provider_totalFunds = Number(formData.get("total-funds"));

  switch (user.role) {
    case "bank-personnel":
      await registerUser({ ...user, role: "BP" }, {
        min_loan_amount: personnel_minLoanAmount,
        max_loan_amount: personnel_maxLoanAmount,
        interest_rate: personnel_interestRate,
        loan_duration: personnel_loanDuration,
      } as BankPersonnel);
      break;

    case "loan-customer":
      await registerUser({ ...user, role: "LC" }, {
        amount: customer_amount,
        term: customer_term,
        interest_rate: customer_interestRate,
      } as LoanCustomer);
      break;
    case "loan-provider":
      await registerUser({ ...user, role: "LP" }, {
        total_funds: provider_totalFunds,
      } as LoanProvider);
      break;
  }
  const cookie = cookies().get("blnk_user")?.value;
  if (!cookie) {
    cookies().set("blnk_user", JSON.stringify(user));
  }

  redirect("/", RedirectType.replace);
}

export async function logout() {
  cookies().delete("blnk_user");
  redirect("/login", RedirectType.replace);
}
export async function login(formData: FormData) {
  const username = formData.get("username")?.toString();

  const users = await getAllUsers();
  const authUser = users.find((user) => user.username === username);
  if (!authUser) {
    throw new Error("User not found");
  }
  cookies().set("blnk_user", JSON.stringify(authUser));
  redirect("/", RedirectType.replace);
}
