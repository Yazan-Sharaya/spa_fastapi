import {getData} from "./request.js";

export class DebugForm {
  constructor() {
    this.debugCard = document.querySelector(".debug-card");
    this.form = this.debugCard.querySelector(".debug-form");

    this.code = this.debugCard.querySelector("code")
    this.originalContent = this.code.innerText

    this.clearButton = this.form.querySelector("button[data-action='clear']");
    this.clearButton.addEventListener("click", this.handleClearClick.bind(this));

    this.sendButton = this.form.querySelector("button[data-action='read']");
    this.sendButton.addEventListener("click", this.handleSendClick.bind(this));

  }
  
  handleClearClick(event) {
    event.preventDefault();
    this.code.innerText = "";
  }

  handleSendClick(event) {
    event.preventDefault();
    const input = document.querySelector("input#endpoint");
    const endpoint = input.value;
    (!endpoint || endpoint === "/") ? this.showResponse(this.originalContent) : getData(endpoint, this.showResponse.bind(this))
  }

  showResponse(data) {
    if (data) {
      data = JSON.parse(data)
      data = JSON.stringify(data, undefined, 2)
    }
    this.code.innerText = data;
  }
}
