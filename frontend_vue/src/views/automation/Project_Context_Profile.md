Project Context Profile

1️⃣ Project Overview

Project Name: Automation Dashboard

Project Type: Workflow & Automation Manager

Tech Stack: Vue.js 3, VueFlow, PrimeVue, Lodash, Django Backend

Goal:
إدارة البرامج، عناصر البرامج، المهام، وإنشاء وتشغيل Workflows مع واجهة تفاعلية وسهلة الاستخدام.

2️⃣ State Management

Programs: إدارة قائمة البرامج، إنشاء، تعديل، حذف.

Program Elements: إدارة عناصر البرامج مثل الأزرار، الصور، النصوص، إلخ.

Workflows: إنشاء Workflows متعددة، تعديل الحالة، حذف، وتشغيل.

Nodes: تمثيل كل خطوة أو إجراء داخل الـ Workflow، مع دعم Node selection والتحديث التفاعلي.

Edges: توصيل Nodes معًا لتمثيل تسلسل الإجراءات.

Tasks: إدارة مهام مرتبطة بالبرامج.

Delays: التعامل مع التأخيرات داخل الإجراءات.

Notes: استخدام ref و reactive لإدارة الحالة، و computed للبيانات المشتقة، مع debounce للحفظ التلقائي.

3️⃣ Components

CustomNode.vue: مكون مخصص لعقدة Workflow.

CustomEdge.vue: مكون مخصص لحواف الـ Workflow.

LiveConsole.vue: مكون لعرض الـ Logs ونتائج تنفيذ الـ Actions.

VueFlow Core Components: VueFlow, Panel, Background, Controls, MiniMap.

Drag & Drop: باستخدام vuedraggable لإنشاء Nodes ديناميكيًا.

4️⃣ Features

CRUD على Programs وProgram Elements

CRUD على Workflows، Nodes، Edges

إنشاء وتشغيل Tasks

Auto-save للعقد مع debounce لتقليل عدد الطلبات للـ Backend

إدارة Actions مرتبطة بالعقد مع إمكانية تعديلها ديناميكيًا

تلوين Nodes حسب نوع الـ Action (Open, Close, Wait, Press, Hotkey)

Visual feedback عبر PrimeVue Toast لجميع الأحداث

5️⃣ Backend Integration

AutomationService API Endpoints:

listPrograms, getProgram, createProgram, updateProgram, deleteProgram

listProgramElements, getProgramElement, createProgramElement, updateProgramElement, deleteProgramElement

listWorkflows, getWorkflow, createWorkflow, updateWorkflow, deleteWorkflow

listWorkflowNodes, createWorkflowNode, updateWorkflowNode, deleteWorkflowNode

createWorkflowEdge, updateWorkflowEdge

runWorkflowNode, runWorkflow

openProgram, closeProgram, focusProgram, maximizeProgram, statusProgram

6️⃣ User Interactions

Drag & Drop: لإنشاء Nodes من البرامج أو عناصر البرامج.

Node Selection & Action Editing: اختيار العقدة وتعديل الـ Action المرتبط بها مباشرة.

Connect Nodes: ربط العقد بواسطة Edges لتحديد تسلسل الإجراءات.

Workflow Start/Stop: تشغيل Workflow بالكامل أو عقد محددة.

Toast Notifications: عرض رسائل نجاح، خطأ، أو معلومات لجميع العمليات.

7️⃣ File Structure

/components/Automation → جميع المكونات المخصصة لعقد وحواف Workflow

/services/AutomationService.js → التعامل مع API الباك اند

/views/AutomationDashboard.vue → الواجهة الرئيسية للمشروع

/assets → ملفات الصور والميديا المرتبطة بالمشروع
