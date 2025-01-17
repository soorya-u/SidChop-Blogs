import { z } from "zod";

export const blogSchema = z.object({
  title: z.string().min(1, { message: "This Field is Required" }),
  content: z
    .string()
    .min(1, { message: "This Field is Required" })
    .min(50, { message: "Content should be minimum of 50 characters" }),
});

export type TBlog = z.infer<typeof blogSchema>;
