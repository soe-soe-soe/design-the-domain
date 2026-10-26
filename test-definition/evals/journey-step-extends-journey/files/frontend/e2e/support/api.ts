/** Setup through the backend API instead of clicks. */
export async function createProjectWithEvidence(title: string): Promise<{ projectUrl: string }> {
  // POST /projects, /procedures, /evidences (omitted in this fixture)
  return { projectUrl: "" };
}
