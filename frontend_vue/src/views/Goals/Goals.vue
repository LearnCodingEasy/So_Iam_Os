<template>
  <div class="workspace-page">
    <header class="workspace-header">
      <div><span class="eyebrow">Planning</span><h1>Goals</h1><p>حوّل أهدافك الكبيرة إلى نتائج واضحة يمكن تنفيذها ومتابعتها.</p></div>
      <button class="primary-btn" @click="openCreate">＋ هدف جديد</button>
    </header>

    <div v-if="error" class="alert error">{{ error }}</div>
    <div v-if="success" class="alert success">{{ success }}</div>

    <section class="stats-grid">
      <article class="stat-card"><span>Active</span><strong>{{ stats.active }}</strong></article>
      <article class="stat-card"><span>Completed</span><strong>{{ stats.completed }}</strong></article>
      <article class="stat-card"><span>Average progress</span><strong>{{ stats.progress }}%</strong></article>
      <article class="stat-card"><span>Overdue</span><strong>{{ stats.overdue }}</strong></article>
    </section>

    <section class="content-card">
      <div class="toolbar"><input v-model="search" placeholder="ابحث في الأهداف..." /><select v-model="statusFilter"><option value="">كل الحالات</option><option value="active">Active</option><option value="paused">Paused</option><option value="completed">Completed</option><option value="cancelled">Cancelled</option><option value="archived">Archived</option></select></div>
      <div v-if="loading" class="loading">جاري تحميل الأهداف...</div>
      <div v-else-if="filteredGoals.length === 0" class="empty">لا توجد أهداف مطابقة.</div>
      <div v-else class="goal-grid">
        <article v-for="goal in filteredGoals" :key="goal.id" class="goal-card">
          <div class="goal-top"><span class="pill" :class="goal.status">{{ goal.status_display || goal.status }}</span><span>{{ goal.priority_display || goal.priority }}</span></div>
          <h3>{{ goal.title }}</h3><p>{{ goal.description || 'بدون وصف' }}</p>
          <div class="progress-row"><span>Progress</span><strong>{{ goal.progress_percent }}%</strong></div><div class="progress"><i :style="{ width: `${goal.progress_percent}%` }"></i></div>
          <div class="goal-meta"><span>📅 {{ goal.target_date || 'No deadline' }}</span><span>✓ {{ goal.completed_task_count || 0 }}/{{ goal.task_count || 0 }} tasks</span></div>
          <div class="card-actions"><button @click="editGoal(goal)">تعديل</button><button v-if="goal.status === 'active'" @click="runGoalAction(goal, 'pause')">إيقاف</button><button v-else-if="goal.status === 'paused'" @click="runGoalAction(goal, 'resume')">استئناف</button><button v-if="goal.status !== 'completed'" @click="runGoalAction(goal, 'complete')">إكمال</button><button class="danger" @click="removeGoal(goal)">حذف</button></div>
        </article>
      </div>
    </section>

    <div v-if="dialog" class="modal-backdrop" @click.self="dialog=false"><form class="modal-card" @submit.prevent="saveGoal"><div class="modal-head"><h2>{{ editing ? 'تعديل الهدف' : 'هدف جديد' }}</h2><button type="button" @click="dialog=false">×</button></div><label>العنوان<input v-model.trim="form.title" required /></label><label>الوصف<textarea v-model="form.description" rows="4"></textarea></label><div class="form-grid"><label>الأولوية<select v-model="form.priority"><option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option><option value="critical">Critical</option></select></label><label>الحالة<select v-model="form.status"><option value="active">Active</option><option value="paused">Paused</option><option value="cancelled">Cancelled</option><option value="archived">Archived</option></select></label><label>البداية<input v-model="form.start_date" type="date" /></label><label>الموعد النهائي<input v-model="form.target_date" type="date" /></label><label>المدة المتوقعة بالدقائق<input v-model.number="form.estimated_minutes" type="number" min="0" /></label><label>نسبة التقدم<input v-model.number="form.progress_percent" type="number" min="0" max="100" /></label></div><div class="modal-actions"><button type="button" @click="dialog=false">إلغاء</button><button class="primary-btn" :disabled="saving">{{ saving ? 'جارٍ الحفظ...' : 'حفظ' }}</button></div></form></div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { completeGoal, createGoal, deleteGoal, listGoals, pauseGoal, resumeGoal, updateGoal, updateGoalProgress } from '@/services/goals'

const goals = ref([]), loading = ref(false), saving = ref(false), dialog = ref(false), editing = ref(null), search = ref(''), statusFilter = ref(''), error = ref(''), success = ref('')
const form = reactive({ title:'', description:'', priority:'medium', status:'active', start_date:'', target_date:'', estimated_minutes:0, progress_percent:0 })
const stats = computed(() => ({ active: goals.value.filter(g=>g.status==='active').length, completed: goals.value.filter(g=>g.status==='completed').length, progress: goals.value.length ? Math.round(goals.value.reduce((a,g)=>a+Number(g.progress_percent||0),0)/goals.value.length) : 0, overdue: goals.value.filter(g=>g.overdue).length }))
const filteredGoals = computed(() => goals.value.filter(g => (!statusFilter.value || g.status===statusFilter.value) && `${g.title} ${g.description}`.toLowerCase().includes(search.value.toLowerCase())))
const load = async () => { loading.value=true; error.value=''; try { goals.value=await listGoals() } catch(e){ error.value=e.response?.data?.detail || 'تعذر تحميل الأهداف.' } finally { loading.value=false } }
const resetForm = () => Object.assign(form,{title:'',description:'',priority:'medium',status:'active',start_date:new Date().toISOString().slice(0,10),target_date:'',estimated_minutes:0,progress_percent:0})
const openCreate=()=>{editing.value=null;resetForm();dialog.value=true}
const editGoal=(g)=>{editing.value=g.id;Object.assign(form,{title:g.title,description:g.description,priority:g.priority,status:g.status,start_date:g.start_date,target_date:g.target_date||'',estimated_minutes:g.estimated_minutes||0,progress_percent:g.progress_percent||0});dialog.value=true}
const saveGoal=async()=>{saving.value=true;error.value='';try{const payload={...form,target_date:form.target_date||null};const saved=editing.value?await updateGoal(editing.value,payload):await createGoal(payload);if(form.progress_percent!==saved.progress_percent) await updateGoalProgress(saved.id,form.progress_percent);dialog.value=false;success.value='تم حفظ الهدف بنجاح.';await load()}catch(e){error.value=e.response?.data?.detail||'تعذر حفظ الهدف.'}finally{saving.value=false}}
const runGoalAction=async(g,action)=>{try{if(action==='pause')await pauseGoal(g.id);if(action==='resume')await resumeGoal(g.id);if(action==='complete')await completeGoal(g.id);success.value='تم تحديث الهدف.';await load()}catch(e){error.value=e.response?.data?.detail||'تعذر تحديث الهدف.'}}
const removeGoal=async(g)=>{if(!window.confirm(`حذف الهدف "${g.title}"؟`))return;try{await deleteGoal(g.id);success.value='تم حذف الهدف.';await load()}catch(e){error.value=e.response?.data?.detail||'تعذر حذف الهدف.'}}
onMounted(load)
</script>

<style scoped>
.workspace-page{min-height:100vh;padding:32px;max-width:1400px;margin:auto;color:var(--text-color,#e5e7eb)}.workspace-header{display:flex;justify-content:space-between;gap:24px;align-items:flex-start;margin-bottom:28px}.eyebrow{color:#60a5fa;font-size:12px;text-transform:uppercase;letter-spacing:.12em}.workspace-header h1{margin:6px 0;font-size:34px}.workspace-header p{margin:0;color:#94a3b8}.primary-btn{background:#2563eb;color:#fff;border:0;border-radius:10px;padding:11px 16px;font-weight:700;cursor:pointer}.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:18px}.stat-card,.content-card,.goal-card{background:var(--surface-card,#111827);border:1px solid var(--surface-border,#253044);border-radius:16px}.stat-card{padding:18px}.stat-card span{display:block;color:#94a3b8;font-size:13px}.stat-card strong{font-size:28px}.content-card{padding:18px}.toolbar{display:flex;gap:10px;margin-bottom:18px}.toolbar input,.toolbar select,.modal-card input,.modal-card select,.modal-card textarea{width:100%;background:#0f172a;color:#e5e7eb;border:1px solid #334155;border-radius:9px;padding:10px}.toolbar input{max-width:500px}.goal-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:15px}.goal-card{padding:18px}.goal-top,.progress-row,.goal-meta,.card-actions{display:flex;justify-content:space-between;gap:8px;align-items:center}.goal-card h3{margin:14px 0 6px}.goal-card p{color:#94a3b8;min-height:42px}.pill{padding:4px 8px;border-radius:999px;background:#334155;font-size:11px}.pill.active{background:#064e3b}.pill.completed{background:#1e3a8a}.progress{height:7px;background:#1f2937;border-radius:999px;overflow:hidden}.progress i{display:block;height:100%;background:#3b82f6}.goal-meta{font-size:12px;color:#94a3b8;margin:12px 0}.card-actions button,.modal-actions button{border:0;background:#1f2937;color:#e5e7eb;padding:8px 10px;border-radius:8px;cursor:pointer}.card-actions .danger{color:#fca5a5}.alert{padding:12px;border-radius:10px;margin-bottom:14px}.alert.error{background:#451a1a;color:#fecaca}.alert.success{background:#052e1b;color:#bbf7d0}.loading,.empty{padding:45px;text-align:center;color:#94a3b8}.modal-backdrop{position:fixed;inset:0;background:#0009;display:grid;place-items:center;padding:20px;z-index:100}.modal-card{width:min(720px,100%);background:#111827;border:1px solid #334155;border-radius:16px;padding:20px;box-shadow:0 25px 80px #0008}.modal-head{display:flex;justify-content:space-between;align-items:center}.modal-head button{background:none;border:0;color:#94a3b8;font-size:24px}.modal-card label{display:block;margin-top:14px;font-size:13px;color:#cbd5e1}.modal-card label input,.modal-card label select,.modal-card label textarea{margin-top:6px}.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.modal-actions{display:flex;justify-content:flex-end;gap:10px;margin-top:20px}@media(max-width:800px){.workspace-page{padding:18px}.workspace-header{flex-direction:column}.stats-grid{grid-template-columns:1fr 1fr}.form-grid{grid-template-columns:1fr}}
</style>
