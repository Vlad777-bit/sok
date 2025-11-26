const KEY = "sok_token";

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
