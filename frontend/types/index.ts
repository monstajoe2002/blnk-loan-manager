export type User = {
  id: string;
  username: string;
  password?: string;
  email: string;
  role: string;
};
export type CreateUser = Partial<User> & { password: string };
export type UpdateUser = Partial<CreateUser> & { id: User["id"] };
export type Role = "bank-personnel" | "loan-customer" | "loan-provider";
export type BankPersonnel = {
  id: string;
  user: User;
  min_loan_amount: number;
  max_loan_amount: number;
  interest_rate: number;
  loan_duration: number;
};
export type LoanCustomer = {
  id: string;
  user: User;
  amount: number;
  term: number;
  interest_rate: number;
};
export type LoanProvider = {
  id: string;
  user: User;
  total_funds: number;
};
export type Loan = {
  id: string;
  loan_provider: LoanProvider;
  loan_customer: LoanCustomer;
  status: string;
};
