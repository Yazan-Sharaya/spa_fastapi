import { People } from "./people.js";
import { DebugForm } from "./debug.js";
import {Notes} from "./notes.js";

function main() {
  new People();
  new Notes();
  if (document.querySelector(".debug-card")) {
    const debug = new DebugForm();
    debug.showResponse("");
  }
}

main();
