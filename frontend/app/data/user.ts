import axios from "axios";
import {
  User,
  CreateUser,
  UpdateUser,
  BankPersonnel,
  LoanCustomer,
  LoanProvider,
} from "../../types";
import { cookies } from "next/headers";
import {
  getBankPersonnelData,
  getLoanCustomerData,
  getLoanProviderData,
} from "./loans";

export const getUser = async (userId: string): Promise<User> => {
  const response = await axios.get(
    `${process.env.NEXT_PUBLIC_API_URL}/api/v1/users/${userId}/`
  );
  return response.data;
};

export const registerUser = async (
  user: CreateUser,
  data: BankPersonnel | LoanCustomer | LoanProvider
): Promise<User> => {
  const response = await axios.post(
    `${process.env.NEXT_PUBLIC_API_URL}/api/v1/users/`,
    { ...user, ...data }
  );

  return response.data;
};

export const updateUser = async (user: UpdateUser): Promise<User> => {
  const response = await axios.patch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/v1/users/${user.id}/`,
    user
  );
  return response.data;
};

export const getLoggedInUser = async (): Promise<User | null> => {
  const userCookie = cookies().get("blnk_user");
  if (!userCookie) {
    return null;
  }
  const username = JSON.parse(userCookie.value).username;
  const users = await getAllUsers();
  const user = users.find((user) => user.username === username);
  if (!user) {
    return null;
  }
  return user;
};

export const getAllUsers = async (): Promise<User[]> => {
  const response = await axios.get(
    `${process.env.NEXT_PUBLIC_API_URL}/api/v1/users/`
  );
  return response.data;
};

export const getUserData = async (
  userId: string
): Promise<BankPersonnel | LoanCustomer | LoanProvider> => {
  let data: BankPersonnel | LoanCustomer | LoanProvider | null = null;
  const user = await getLoggedInUser();
  switch (user?.role) {
    case "BP":
      data = await getBankPersonnelData(userId);
      break;
    case "LC":
      data = await getLoanCustomerData(userId);
      break;
    case "LP":
      data = await getLoanProviderData(userId);
      break;
  }
  return data as BankPersonnel | LoanCustomer | LoanProvider;
};
