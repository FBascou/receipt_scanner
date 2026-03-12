export const handleShowPasswordButton = (
  passwordButton: HTMLButtonElement | null,
  passwordInput: HTMLInputElement | null,
) => {
  return passwordButton?.addEventListener("click", (event: Event) => {
    event.preventDefault();

    if (!passwordInput || !passwordButton) return;

    const isPassword = passwordInput.type === "password";

    passwordInput.type = isPassword ? "text" : "password";
    passwordButton.textContent = isPassword ? "X" : "O";
  });
};
