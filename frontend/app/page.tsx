import { getLoggedInUser, getUserData } from "./data/user";
import { logout } from "./actions/user";
export default async function Home() {
  const user = await getLoggedInUser();
  const userData = await getUserData(user?.id || "");
  return (
    <div>
      <h1>blnk Loan Manager</h1>
      <nav className="flex justify-between mt-4">
        <span className="font-medium">Hello, {user?.username}!</span>
        <form action={logout}>
          <button
            type="submit"
            className="text-blue-500 bg-inherit p-0 hover:bg-inherit hover:text-blue-600 hover:underline"
          >
            Logout
          </button>
        </form>
      </nav>
      <pre>{JSON.stringify(userData, null, 2)}</pre>
    </div>
  );
}
