const KEY = "dev_secret_change_me";

export const auth = {
  getToken() {
    return localStorage.getItem(KEY) || "";
  },
  setToken(token) {
    localStorage.setItem(KEY, token);
  },
  clear() {
    localStorage.removeItem(KEY);
  },
  isAuthed() {
    return !!this.getToken();
  }
};
