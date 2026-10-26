import { Page } from "@playwright/test";

export class LoginPage {
  constructor(private readonly page: Page) {}
  async login(email: string, password: string): Promise<void> {
    // Auth0 login (omitted in this fixture)
  }
}
