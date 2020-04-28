class Metadata(dict):
    @property
    def tenant_id(self):
        return self.get('tenant_id')

    @property
    def action(self):
        return self.get('action')
