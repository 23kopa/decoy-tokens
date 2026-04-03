export function tokensList() {
  return {
    search: '',
    selectedType: '',

    normalize(value) {
      return String(value || '').trim().toLowerCase();
    },

    matchesToken(el) {
      const name = this.normalize(el.dataset.tokenName);
      const type = this.normalize(el.dataset.tokenType);

      const search = this.normalize(this.search);
      const selectedType = this.normalize(this.selectedType);

      const matchesSearch = !search || name.includes(search);
      const matchesType = !selectedType || type === selectedType;

      return matchesSearch && matchesType;
    },

    clearFilters() {
      this.search = '';
      this.selectedType = '';
    },
  };
}