enum Role {
  BP = "bank-personnel",
  LC = "loan-customer",
  LP = "loan-provider",
}
export const ROLE_SLUGS = Object.values(Role);
export const ROLE_VALUES = Object.keys(Role);
export const ROLE_LABELS = Object.values(Role).map((role) => {
  return {
    value: role,
    label: role.replace("-", " "),
  };
});
