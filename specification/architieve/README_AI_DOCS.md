# 📚 AI-Assisted Development Documentation

## 🎯 Tổng Quan

Bộ tài liệu này được thiết kế để giúp các công cụ AI coding (Cursor AI, GitHub Copilot, Cline, ChatGPT, Claude, etc.) và developers làm việc hiệu quả hơn với dự án FastAPI Backend này.

---

## 📂 Cấu Trúc Tài Liệu

### 1. **PROJECT_SUMMARY.md** 🎯
**Mục đích:** Tổng quan nhanh về toàn bộ dự án  
**Dành cho:** Everyone (Developers, Managers, AI Assistants)  
**Nội dung:**
- Executive summary
- Tech stack overview
- Security architecture diagram
- Key features highlights
- Project status
- Quick start guide

**Khi nào sử dụng:**
- First document to read
- Quick reference
- Onboarding new team members
- Project presentation

---

### 2. **BACKEND_ARCHITECTURE_SPECIFICATION.md** 📐
**Mục đích:** Đặc tả kiến trúc tổng thể  
**Dành cho:** Technical Leads, Architects, Senior Developers  
**Nội dung:**
- Kiến trúc Clean Architecture chi tiết
- Cấu trúc thư mục đầy đủ
- Phân tầng và trách nhiệm từng layer
- Security implementation (Authentication, Authorization, Validation)
- Cấu hình production-ready
- Best practices và patterns

**Khi nào sử dụng:**
- Khi cần hiểu tổng quan về dự án
- Khi thiết kế features mới lớn
- Khi onboarding team members mới
- Khi review architecture

---

### 3. **SECURITY_ARCHITECTURE.md** 🔐
**Mục đích:** Security implementation guide  
**Dành cho:** Security Engineers, Backend Developers  
**Nội dung:**
- Complete security stack (FastAPI-Users, Authlib, Casbin)
- Authentication setup (Email/Password, OAuth2 social login)
- Authorization with Casbin (RBAC/ABAC/ACL)
- Data validation with Pydantic V2
- Password security (Bcrypt)
- JWT token handling
- Common security scenarios
- Security best practices
- Production checklist

**Khi nào sử dụng:**
- Implementing authentication
- Setting up authorization
- Adding OAuth2 social login
- Security review
- Compliance requirements

---

### 4. **.cursorrules** 🎯
**Mục đích:** Hướng dẫn cho Cursor AI  
**Dành cho:** Cursor AI Editor  
**Nội dung:**
- Project context và architecture layers
- Coding standards (Python, FastAPI, SQLAlchemy, Pydantic)
- File naming conventions
- Import organization
- Error handling patterns
- Common tasks workflow

**Khi nào sử dụng:**
- Tự động được Cursor AI đọc
- Giúp Cursor generate code đúng patterns
- Cải thiện code suggestions

---

### 5. **.github/copilot-instructions.md** 🤖
**Mục đích:** Hướng dẫn cho GitHub Copilot  
**Dành cho:** GitHub Copilot  
**Nội dung:**
- Code generation guidelines
- Type hints requirements
- Async/await patterns
- Pydantic V2 và SQLAlchemy 2.0 syntax
- Complete CRUD feature snippets
- Repository và Service patterns
- Testing patterns

**Khi nào sử dụng:**
- Tự động được Copilot sử dụng
- Khi cần suggestions chính xác
- Khi generate boilerplate code

---

### 6. **LLM_CODING_GUIDE.md** 📖
**Mục đích:** Universal guide cho tất cả LLM assistants  
**Dành cho:** ChatGPT, Claude, Cline, và mọi AI coding assistant  
**Nội dung:**
- Core principles
- Architecture layers chi tiết
- Code patterns với examples
- Anti-patterns cần tránh
- Quick reference
- Common issues & solutions
- Security checklist
- Performance optimization

**Khi nào sử dụng:**
- Khi chat với AI assistants
- Khi cần giải thích patterns
- Khi debug issues
- Khi refactor code

---

### 7. **CODE_TEMPLATES.md** 📝
**Mục đích:** Templates sẵn sàng sử dụng  
**Dành cho:** Developers và AI assistants  
**Nội dung:**
- Complete CRUD feature template (Product example)
- Pydantic schemas với validation
- SQLAlchemy models với relationships
- Repository với complex queries
- Service với business logic
- API routes với documentation
- Testing examples
- Common patterns

**Khi nào sử dụng:**
- Khi tạo feature mới
- Khi cần copy-paste templates
- Khi cần examples cụ thể
- Khi training team members

---

### 8. **QUICK_SNIPPETS.md** ⚡
**Mục đích:** Snippets nhanh cho các tác vụ thường gặp  
**Dành cho:** Developers và AI assistants  
**Nội dung:**
- CRUD resource creation (step-by-step)
- Database query snippets
- Test snippets
- Pydantic validators
- SQLAlchemy relationships
- Authentication snippets
- Background tasks
- File upload

**Khi nào sử dụng:**
- Khi cần code nhanh
- Khi tạo feature cơ bản
- Khi cần reference syntax
- Khi học patterns mới

---

### 9. **.ai-project-context.json** 🗂️
**Mục đích:** Machine-readable project context  
**Dành cho:** AI tools và automation  
**Nội dung:**
- Project metadata
- Technologies và versions
- Code patterns definitions
- Naming conventions
- Layer dependencies rules
- Required patterns
- Common tasks workflows
- Testing guidelines
- Security checklist
- Helpful commands

**Khi nào sử dụng:**
- Được AI tools parse tự động
- Khi integrate với IDE extensions
- Khi build automation tools
- Khi validate code structure

---

## 📊 Document Reading Order

### For New Team Members:
```
1. PROJECT_SUMMARY.md          ← Start here! (10 min)
2. BACKEND_ARCHITECTURE...md   ← Deep dive (30 min)
3. SECURITY_ARCHITECTURE.md    ← Security (20 min)
4. CODE_TEMPLATES.md           ← Practical examples (15 min)
5. QUICK_SNIPPETS.md           ← Quick reference (5 min)
```

### For Security Review:
```
1. PROJECT_SUMMARY.md          ← Overview
2. SECURITY_ARCHITECTURE.md    ← Complete security guide
3. BACKEND_ARCHITECTURE...md   ← Security implementation details
```

### For AI Assistant Setup:
```
1. .cursorrules                ← For Cursor AI
2. .github/copilot-inst...md   ← For GitHub Copilot
3. LLM_CODING_GUIDE.md         ← For ChatGPT/Claude/Cline
4. .ai-project-context.json    ← For all AI tools
```

---

## 🚀 Cách Sử Dụng Với Các Công Cụ

### 💻 Cursor AI

**Setup:**
1. File `.cursorrules` được đọc tự động
2. Không cần config gì thêm

**Sử dụng:**
- `Cmd+K` → AI sẽ follow .cursorrules
- `Cmd+L` → Chat với context từ .cursorrules
- Code suggestions tự động theo patterns

**Tips:**
- Mention "follow project patterns" trong prompts
- Reference specific patterns: "create CRUD following repository pattern"

---

### 🐙 GitHub Copilot

**Setup:**
1. File `.github/copilot-instructions.md` được đọc tự động
2. Enable Copilot trong VS Code/IDE

**Sử dụng:**
- Copilot suggestions sẽ follow instructions
- Tab để accept suggestions
- Cmd+→ để xem alternatives

**Tips:**
- Viết docstrings trước, Copilot sẽ generate implementation
- Type function signature, Copilot complete body
- Comment "# Create user repository with..." để get better suggestions

---

### 💬 ChatGPT / Claude

**Setup:**
1. Copy relevant sections từ `LLM_CODING_GUIDE.md`
2. Hoặc share cả file để establish context

**Sử dụng:**
```
[Paste LLM_CODING_GUIDE.md content]

Now help me create a CRUD feature for "Order" resource.
```

**Tips:**
- Start conversation với guide để set context
- Reference specific patterns: "following the Service pattern in the guide"
- Ask to "follow the project standards"

---

### 🤖 Cline (Claude in VS Code)

**Setup:**
1. Cline có thể đọc project files
2. Reference `.cursorrules` và `LLM_CODING_GUIDE.md`

**Sử dụng:**
```
@file .cursorrules @file LLM_CODING_GUIDE.md

Create CRUD endpoints for Product following our patterns.
```

**Tips:**
- Use @file để reference guides
- Cline có thể edit multiple files
- Ask to "follow .cursorrules"

---

### 🔧 Windsurf / Other IDEs

**Setup:**
- Copy `.cursorrules` content vào IDE settings
- Hoặc reference guides trong prompts

**Sử dụng:**
- Similar to Cursor AI workflow
- Paste relevant guide sections khi cần

---

## 📖 Workflows Thông Dụng

### Workflow 1: Tạo CRUD Feature Mới

**Bước 1:** Đọc template
```bash
# Xem template trong CODE_TEMPLATES.md hoặc QUICK_SNIPPETS.md
```

**Bước 2:** Với AI Assistant (Cursor/Copilot/ChatGPT)
```
Create CRUD endpoints for "Category" with these fields:
- name: string (required, unique, max 100)
- description: optional string (max 500)
- is_active: boolean (default true)

Follow our project patterns:
- Use Pydantic V2 for schemas
- Use SQLAlchemy 2.0 for models
- Implement repository pattern
- Add service layer with business logic
- Create API routes with authentication
- Include tests
```

**Bước 3:** AI sẽ generate theo đúng patterns:
- Schema → Model → Repository → Service → API → Tests

**Bước 4:** Review và adjust
- Kiểm tra type hints
- Kiểm tra async/await
- Kiểm tra error handling
- Run tests

---

### Workflow 2: Debug Issue

**Với AI Assistant:**
```
I'm getting this error: [paste error]

Context:
- File: app/services/user_service.py
- Function: create_user
- Following patterns from LLM_CODING_GUIDE.md

The code:
[paste code]

Help me debug this following our project standards.
```

AI sẽ:
- Check async/await usage
- Check type hints
- Check error handling
- Suggest fixes theo patterns

---

### Workflow 3: Refactor Existing Code

**Với AI Assistant:**
```
@file .cursorrules

Refactor this code to follow Clean Architecture:
[paste code]

Requirements:
- Move business logic to service layer
- Use repository pattern
- Add proper type hints
- Add error handling
- Keep existing functionality
```

---

### Workflow 4: Add Complex Query

**Reference QUICK_SNIPPETS.md:**
```
Need to add search functionality with filters:
- Search by name (LIKE)
- Filter by is_active
- Filter by date range
- Paginate results

Use the query patterns from QUICK_SNIPPETS.md
```

AI sẽ generate theo repository pattern với:
- Proper SQLAlchemy 2.0 syntax
- Async/await
- Type hints
- Pagination support

---

## 🎓 Best Practices Khi Làm Việc Với AI

### ✅ DO:

1. **Reference cụ thể:**
   ```
   "Follow the Repository pattern from LLM_CODING_GUIDE.md"
   ```

2. **Provide context:**
   ```
   "This is a FastAPI project using SQLAlchemy 2.0 async"
   ```

3. **Ask for complete implementations:**
   ```
   "Generate complete CRUD feature including tests"
   ```

4. **Request explanations:**
   ```
   "Explain why we use this pattern"
   ```

5. **Ask for alternatives:**
   ```
   "Show me 3 ways to implement this"
   ```

### ❌ DON'T:

1. **Vague requests:**
   ```
   ❌ "Create user endpoint"
   ✅ "Create user CRUD following our service/repository pattern"
   ```

2. **Accept code blindly:**
   - Always review generated code
   - Check patterns compliance
   - Run tests

3. **Mix old syntax:**
   ```
   ❌ "Use Pydantic" (unclear version)
   ✅ "Use Pydantic V2 with model_config"
   ```

4. **Skip error handling:**
   - Always ask AI to include error handling
   - Request appropriate HTTP status codes

5. **Ignore types:**
   ```
   ❌ Accept code without type hints
   ✅ Request "add complete type hints"
   ```

---

## 🔍 Tips & Tricks

### Tip 1: Multi-file Features
```
@file CODE_TEMPLATES.md

Create Order feature with:
1. Schema (OrderCreate, OrderUpdate, OrderResponse)
2. Model with relationships to User and Product
3. Repository with complex queries
4. Service with business logic
5. API routes with auth
6. Tests

Generate all files.
```

### Tip 2: Incremental Development
```
Step 1: "Create schema for Order"
[review]

Step 2: "Create model for Order"
[review]

Step 3: "Create repository"
[review and so on...]
```

### Tip 3: Learn Patterns
```
"Explain the Repository pattern used in this project"
"Why do we separate service and repository layers?"
"Show me examples of good vs bad separation of concerns"
```

### Tip 4: Code Review
```
"Review this code against our project standards:
@file .cursorrules
[paste code]

Check for:
- Pattern compliance
- Type hints
- Error handling
- Async/await usage"
```

### Tip 5: Testing Strategy
```
@file QUICK_SNIPPETS.md

Generate tests for Order CRUD:
- Happy path tests
- Error cases (404, 400, 422)
- Edge cases
- Authentication tests

Follow test patterns from snippets.
```

---

## 📊 Cheat Sheet

### Khi Tạo Feature Mới:
1. Reference `CODE_TEMPLATES.md` 
2. Copy template structure
3. Customize cho resource của bạn
4. Chạy migration
5. Write tests
6. Test manually tại `/docs`

### Khi Debug:
1. Check `LLM_CODING_GUIDE.md` Common Issues
2. Review patterns compliance
3. Check logs
4. Verify database connection
5. Check environment variables

### Khi Cần Quick Code:
1. Mở `QUICK_SNIPPETS.md`
2. Copy relevant snippet
3. Customize
4. Paste vào code

### Khi Refactor:
1. Reference `.cursorrules`
2. Identify anti-patterns
3. Ask AI to refactor theo patterns
4. Keep tests passing
5. Review changes

---

## 🎯 Kết Luận

Bộ tài liệu này được thiết kế để:
- ✅ Giảm thiểu code repetitive
- ✅ Đảm bảo consistency
- ✅ Tăng tốc development
- ✅ Cải thiện code quality
- ✅ Giúp AI assistants hiểu project
- ✅ Dễ dàng onboard members mới

**Hãy sử dụng chúng thường xuyên để có experience tốt nhất!** 🚀

---

## 📞 Góp Ý & Câu Hỏi

Nếu có suggestions để improve documentation:
1. Tạo issue/ticket
2. Đề xuất improvements
3. Share experiences

**Happy Coding with AI Assistants! 🤖✨**
