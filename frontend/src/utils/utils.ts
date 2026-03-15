import z from "zod";

export function getFormValues(form: HTMLFormElement) {
  const formData = new FormData(form);
  const data: Record<string, unknown> = {};

  formData.forEach((value, key) => {
    if (value instanceof File) {
      if (!data[key]) {
        data[key] = formData.getAll(key);
      }
    } else {
      data[key] = value;
    }
  });

  return data;
}

export function handleForm(form: HTMLFormElement, schema: z.ZodSchema) {
  const inputs = form.querySelectorAll<HTMLInputElement>("input");

  function validate() {
    const data = getFormValues(form);
    const result = schema.safeParse(data);
    const errors = result.success ? {} : z.flattenError(result.error).fieldErrors;

    inputs.forEach((input) => {
      const errorEl = document.getElementById(`${input.name}-error`) as HTMLParagraphElement | null;
      const message = errors[input.name as keyof typeof errors]?.[0];

      if (message) {
        input.style.borderBottom = "var(--border-error)";
        if (errorEl) errorEl.textContent = message;
      } else {
        input.style.borderBottom = "none";
        if (errorEl) errorEl.textContent = "";
      }
    });

    return result.success;
  }

  form.addEventListener("input", validate);

  form.addEventListener("submit", (event) => {
    const valid = validate();

    if (!valid) {
      event.preventDefault();
    }
  });
}
