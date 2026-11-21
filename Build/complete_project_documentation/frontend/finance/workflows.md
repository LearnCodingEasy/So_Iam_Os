# finance workflows

## Routed screens and source evidence

- Route /finance (finance) is declared at router/index.js:L190; metadata: requiresAuth.

### views/finance/FinanceView.vue
import { computed, onMounted, ref } from 'vue'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import api from '@/services/Shared/api'
import { financeApi } from '@/services/Finance/finance'
import FinanceHero from '@/components/finance/FinanceHero.vue'
import FinanceKpiGrid from '@/components/finance/FinanceKpiGrid.vue'
import FinanceHealthAlerts from '@/components/finance/FinanceHealthAlerts.vue'
import FinanceSectionNav from '@/components/finance/FinanceSectionNav.vue'
import FinanceOverview from '@/components/finance/FinanceOverview.vue'
import FinanceTransactions from '@/components/finance/FinanceTransactions.vue'
import FinanceBudgets from '@/components/finance/FinanceBudgets.vue'


**UNKNOWN:** End-to-end transitions and error outcomes are not runtime verified.
