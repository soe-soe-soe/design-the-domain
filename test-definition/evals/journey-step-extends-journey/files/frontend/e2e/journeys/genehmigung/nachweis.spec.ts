import { test, expect, Page } from "@playwright/test";
import { LoginPage } from "../../pages/LoginPage";
import { PermitsPage } from "../../pages/PermitsPage";
import { createProjectWithEvidence } from "../../support/api";

/** Journey of a Nachweis: its life cycle on the happy path, one step per story. */
test.describe.serial("Nachweis", () => {
  let page: Page;
  let permitsPage: PermitsPage;

  test.beforeAll(async ({ browser }) => {
    page = await browser.newPage();
    await new LoginPage(page).login(process.env.E2E_ADMIN_EMAIL!, process.env.E2E_ADMIN_PASSWORD!);
    const { projectUrl } = await createProjectWithEvidence("Schallgutachten");
    permitsPage = new PermitsPage(page);
    await permitsPage.gotoNachweise(projectUrl);
  });

  test("Nachweis wird beauftragt", { tag: "@US-0031" }, async () => {
    await permitsPage.transitionEvidence("Schallgutachten", "Beauftragen");
    await expect(permitsPage.evidenceStatus("Schallgutachten")).toHaveText("Beauftragt");
  });

  test("Nachweis wird geliefert", { tag: "@US-0031" }, async () => {
    await permitsPage.transitionEvidence("Schallgutachten", "Geliefert");
    await expect(permitsPage.evidenceStatus("Schallgutachten")).toHaveText("Geliefert");
  });

  test("Nachweis geht in Prüfung", { tag: "@US-0033" }, async () => {
    await permitsPage.transitionEvidence("Schallgutachten", "Prüfung starten");
    await expect(permitsPage.evidenceStatus("Schallgutachten")).toHaveText("In Prüfung");
  });
});
