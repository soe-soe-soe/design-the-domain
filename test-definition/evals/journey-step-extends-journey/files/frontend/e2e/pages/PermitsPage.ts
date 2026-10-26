import { Page, Locator } from "@playwright/test";

/** Modul Genehmigung: Seite "Nachweise" eines Antrags. */
export class PermitsPage {
  constructor(private readonly page: Page) {}

  async gotoNachweise(projectUrl: string): Promise<void> {
    await this.page.goto(projectUrl.replace(/\/overview$/, "/permits/first/evidences"));
    await this.page.getByRole("heading", { name: "Nachweise", exact: true }).waitFor();
  }

  /** Zeile eines Nachweises in der Liste, über seinen Titel */
  evidenceRow(title: string): Locator {
    return this.page.getByRole("row", { name: new RegExp(title) });
  }

  /** Statuszelle eines Nachweises */
  evidenceStatus(title: string): Locator {
    return this.evidenceRow(title).getByRole("cell", { name: /status/i });
  }

  /** Führt eine benannte Statusaktion am Nachweis aus, z. B. "Beauftragen" */
  async transitionEvidence(title: string, action: string): Promise<void> {
    await this.evidenceRow(title).getByRole("button", { name: "Aktionen" }).click();
    await this.page.getByRole("menuitem", { name: action }).click();
  }
}
