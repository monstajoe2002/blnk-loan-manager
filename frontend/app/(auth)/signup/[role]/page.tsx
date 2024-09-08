import RegisterUserForm from "@/components/register-user-form";
import { Role } from "@/types";

export default function RolePage({
  params: { role },
}: {
  params: { role: string };
}) {
  return (
    <div>
      <h1>Sign up as a {role.replace("-", " ")}</h1>
      <RegisterUserForm role={role as Role} />
    </div>
  );
}
