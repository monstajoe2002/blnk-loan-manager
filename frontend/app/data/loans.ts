import { Loan, LoanCustomer, LoanProvider } from "@/types";
import axios from "axios";
import { getUser } from "./user";
import { BankPersonnel } from "@/types";
export const getProviderApplications = async (): Promise<Loan[]> => {
  const response = await axios.get(
    `${process.env.NEXT_PUBLIC_API_URL}/api/v1/providers/applications/`
  );
  return response.data;
};

export const getBankPersonnelData = async (userId: string) => {
  const user = await getUser(userId);
  const { data } = await axios.get(
    `${process.env.NEXT_PUBLIC_API_URL}/api/v1/personnels/`
  );
  const personnel = data.find(
    (personnel: BankPersonnel) => personnel.user.id === user.id
  );
  return personnel;
};

export const getLoanCustomerData = async (userId: string) => {
  const user = await getUser(userId);
  const { data } = await axios.get(
    `${process.env.NEXT_PUBLIC_API_URL}/api/v1/customers/`
  );
  const customer = data.find(
    (customer: LoanCustomer) => customer.user.id === user.id
  );
  return customer;
};

export const getLoanProviderData = async (userId: string) => {
  const user = await getUser(userId);
  const { data } = await axios.get(
    `${process.env.NEXT_PUBLIC_API_URL}/api/v1/providers/`
  );
  const provider = data.find(
    (provider: LoanProvider) => provider.user.id === user.id
  );
  return provider;
};
