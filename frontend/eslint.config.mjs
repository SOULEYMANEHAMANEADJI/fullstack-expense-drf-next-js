import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
  {
    ignores: [
      "**/page_backup_old.tsx",
      "**/page_old.tsx",
      "**/*_old.tsx",
      "**/*_backup*.tsx",
    ],
  },
];

export default eslintConfig;
