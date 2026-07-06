from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import uuid4

app = FastAPI(title="招聘平台 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Job(BaseModel):
    id: str
    title: str
    company: str
    city: str
    salary_min: int
    salary_max: int
    experience: str
    education: str
    tags: List[str]
    description: str
    requirements: str
    contact_email: str
    status: str
    created_at: datetime
    updated_at: datetime


class Candidate(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    education: str
    experience: str
    resume: str
    skills: List[str]
    desired_job: str
    desired_city: str
    status: str
    created_at: datetime


class Application(BaseModel):
    id: str
    job_id: str
    candidate_id: str
    status: str
    cover_letter: str
    applied_at: datetime
    updated_at: datetime


class Message(BaseModel):
    id: str
    application_id: str
    sender_id: str
    sender_type: str
    content: str
    sent_at: datetime


class Interview(BaseModel):
    id: str
    application_id: str
    interviewer: str
    round: str
    method: str
    time: datetime
    location: str
    status: str
    notes: str
    created_at: datetime
    updated_at: datetime


class Offer(BaseModel):
    id: str
    application_id: str
    interview_id: Optional[str]
    salary_min: int
    salary_max: int
    position_title: str
    start_date: datetime
    notes: str
    status: str
    created_at: datetime
    updated_at: datetime


class Stats(BaseModel):
    total_jobs: int
    active_jobs: int
    total_applications: int
    pending_applications: int
    communicating_applications: int
    interviewing_applications: int
    hired_applications: int
    rejected_applications: int
    total_interviews: int
    scheduled_interviews: int
    completed_interviews: int
    cancelled_interviews: int
    pending_interviews: int
    total_offers: int
    pending_offers: int
    accepted_offers: int
    rejected_offers: int
    withdrawn_offers: int
    pending_onboarding_offers: int


mock_jobs = [
    {
        "id": "job-001",
        "title": "高级前端工程师",
        "company": "字节跳动",
        "city": "北京",
        "salary_min": 30000,
        "salary_max": 50000,
        "experience": "3-5年",
        "education": "本科",
        "tags": ["Vue", "React", "TypeScript"],
        "description": "负责公司核心产品的前端开发，参与技术选型和架构设计",
        "requirements": "1. 3年以上前端开发经验\n2. 精通Vue/React框架\n3. 熟悉TypeScript\n4. 有大型项目经验者优先",
        "contact_email": "hr@bytedance.com",
        "status": "active",
        "created_at": "2026-06-01T10:00:00",
        "updated_at": "2026-06-15T14:30:00"
    },
    {
        "id": "job-002",
        "title": "后端开发工程师",
        "company": "阿里巴巴",
        "city": "杭州",
        "salary_min": 28000,
        "salary_max": 45000,
        "experience": "2-4年",
        "education": "本科",
        "tags": ["Python", "Java", "微服务"],
        "description": "负责电商平台后端服务开发，保障系统稳定性和性能",
        "requirements": "1. 2年以上后端开发经验\n2. 精通Python或Java\n3. 熟悉微服务架构\n4. 有高并发经验者优先",
        "contact_email": "hr@alibaba.com",
        "status": "active",
        "created_at": "2026-06-05T09:00:00",
        "updated_at": "2026-06-20T16:00:00"
    },
    {
        "id": "job-003",
        "title": "产品经理",
        "company": "腾讯",
        "city": "深圳",
        "salary_min": 25000,
        "salary_max": 40000,
        "experience": "2-3年",
        "education": "本科",
        "tags": ["B端产品", "用户增长", "数据分析"],
        "description": "负责社交产品的功能规划和迭代，推动产品优化",
        "requirements": "1. 2年以上产品经理经验\n2. 有社交产品经验优先\n3. 良好的数据分析能力\n4. 出色的沟通协调能力",
        "contact_email": "hr@tencent.com",
        "status": "active",
        "created_at": "2026-06-10T11:00:00",
        "updated_at": "2026-06-25T10:00:00"
    },
    {
        "id": "job-004",
        "title": "UI设计师",
        "company": "美团",
        "city": "上海",
        "salary_min": 18000,
        "salary_max": 30000,
        "experience": "1-3年",
        "education": "大专",
        "tags": ["Figma", "UI设计", "用户体验"],
        "description": "负责外卖平台的界面设计，提升用户体验",
        "requirements": "1. 1年以上UI设计经验\n2. 精通Figma/Sketch\n3. 有互联网产品设计经验\n4. 良好的审美能力",
        "contact_email": "hr@meituan.com",
        "status": "closed",
        "created_at": "2026-05-15T08:00:00",
        "updated_at": "2026-06-30T12:00:00"
    }
]

mock_candidates = [
    {
        "id": "candidate-001",
        "name": "张三",
        "email": "zhangsan@example.com",
        "phone": "13800138001",
        "education": "本科",
        "experience": "3年",
        "resume": "张三的个人简历内容...\n\n工作经历：\n2023-至今 XX公司 前端工程师\n2021-2023 YY公司 前端开发\n\n技能：Vue, React, TypeScript, Node.js\n\n项目经验：\n1. 电商平台前端重构 - 负责核心页面开发\n2. 内部管理系统 - 独立完成前端架构设计",
        "skills": ["Vue", "React", "TypeScript", "Node.js", "Webpack"],
        "desired_job": "前端工程师",
        "desired_city": "北京",
        "status": "active",
        "created_at": "2026-06-01T08:00:00"
    },
    {
        "id": "candidate-002",
        "name": "李四",
        "email": "lisi@example.com",
        "phone": "13800138002",
        "education": "硕士",
        "experience": "4年",
        "resume": "李四的个人简历内容...\n\n工作经历：\n2022-至今 XX公司 后端架构师\n2020-2022 YY公司 后端工程师\n\n技能：Python, Java, Redis, MySQL, Docker\n\n项目经验：\n1. 微服务架构改造 - 主导技术选型\n2. 高并发系统优化 - 提升系统吞吐量300%",
        "skills": ["Python", "Java", "Redis", "MySQL", "Docker", "Kubernetes"],
        "desired_job": "后端开发工程师",
        "desired_city": "杭州",
        "status": "active",
        "created_at": "2026-06-05T09:00:00"
    },
    {
        "id": "candidate-003",
        "name": "王五",
        "email": "wangwu@example.com",
        "phone": "13800138003",
        "education": "本科",
        "experience": "2年",
        "resume": "王五的个人简历内容...\n\n工作经历：\n2024-至今 XX公司 产品助理\n2023-2024 YY公司 运营专员\n\n技能：产品设计, 用户调研, 数据分析\n\n项目经验：\n1. 用户增长项目 - 负责需求调研和方案设计\n2. 功能迭代优化 - 提升用户留存率20%",
        "skills": ["产品设计", "用户调研", "数据分析", "Axure", "Excel"],
        "desired_job": "产品经理",
        "desired_city": "深圳",
        "status": "active",
        "created_at": "2026-06-10T10:00:00"
    },
    {
        "id": "candidate-004",
        "name": "赵六",
        "email": "zhaoliu@example.com",
        "phone": "13800138004",
        "education": "大专",
        "experience": "1年",
        "resume": "赵六的个人简历内容...\n\n工作经历：\n2025-至今 XX公司 UI设计师\n\n技能：Figma, Sketch, Illustrator, Photoshop\n\n项目经验：\n1. App界面设计 - 完成全套UI设计\n2. 品牌视觉升级 - 制定设计规范",
        "skills": ["Figma", "Sketch", "UI设计", "用户体验", "插画"],
        "desired_job": "UI设计师",
        "desired_city": "上海",
        "status": "active",
        "created_at": "2026-06-15T11:00:00"
    },
    {
        "id": "candidate-005",
        "name": "钱七",
        "email": "qianqi@example.com",
        "phone": "13800138005",
        "education": "本科",
        "experience": "5年",
        "resume": "钱七的个人简历内容...\n\n工作经历：\n2021-至今 XX公司 技术总监\n2019-2021 YY公司 技术经理\n\n技能：架构设计, 团队管理, Python, Go\n\n项目经验：\n1. 大型系统架构设计 - 支撑千万级用户\n2. 团队建设 - 带领20人技术团队",
        "skills": ["Python", "Go", "架构设计", "团队管理", "微服务"],
        "desired_job": "技术总监",
        "desired_city": "北京",
        "status": "inactive",
        "created_at": "2026-05-20T09:00:00"
    }
]

mock_applications = [
    {
        "id": "app-001",
        "job_id": "job-001",
        "candidate_id": "candidate-001",
        "status": "pending",
        "cover_letter": "您好，我对这个职位非常感兴趣，希望能有机会加入贵公司。",
        "applied_at": "2026-06-20T14:00:00",
        "updated_at": "2026-06-20T14:00:00"
    },
    {
        "id": "app-002",
        "job_id": "job-002",
        "candidate_id": "candidate-002",
        "status": "communicating",
        "cover_letter": "我有丰富的后端开发经验，期待与贵公司合作。",
        "applied_at": "2026-06-22T10:00:00",
        "updated_at": "2026-06-25T16:30:00"
    },
    {
        "id": "app-003",
        "job_id": "job-003",
        "candidate_id": "candidate-003",
        "status": "interviewing",
        "cover_letter": "我对产品经理职位很感兴趣，希望能有面试机会。",
        "applied_at": "2026-06-24T09:00:00",
        "updated_at": "2026-06-28T11:00:00"
    },
    {
        "id": "app-004",
        "job_id": "job-001",
        "candidate_id": "candidate-002",
        "status": "rejected",
        "cover_letter": "前端也是我的强项之一，希望能考虑。",
        "applied_at": "2026-06-18T16:00:00",
        "updated_at": "2026-06-22T10:00:00"
    },
    {
        "id": "app-005",
        "job_id": "job-003",
        "candidate_id": "candidate-001",
        "status": "pending",
        "cover_letter": "虽然我是技术背景，但对产品也很感兴趣。",
        "applied_at": "2026-06-26T13:00:00",
        "updated_at": "2026-06-26T13:00:00"
    }
]

mock_messages = [
    {
        "id": "msg-001",
        "application_id": "app-002",
        "sender_id": "candidate-002",
        "sender_type": "candidate",
        "content": "您好，请问面试安排什么时候能确定？",
        "sent_at": "2026-06-25T14:00:00"
    },
    {
        "id": "msg-002",
        "application_id": "app-002",
        "sender_id": "company-alibaba",
        "sender_type": "company",
        "content": "您好，我们正在安排，预计下周会有消息。",
        "sent_at": "2026-06-25T16:30:00"
    },
    {
        "id": "msg-003",
        "application_id": "app-003",
        "sender_id": "company-tencent",
        "sender_type": "company",
        "content": "恭喜您进入面试环节，请确认下周二下午2点是否方便？",
        "sent_at": "2026-06-28T10:00:00"
    },
    {
        "id": "msg-004",
        "application_id": "app-003",
        "sender_id": "candidate-003",
        "sender_type": "candidate",
        "content": "方便的，没问题。",
        "sent_at": "2026-06-28T11:00:00"
    }
]

mock_interviews = [
    {
        "id": "interview-001",
        "application_id": "app-003",
        "interviewer": "李明",
        "round": "初试",
        "method": "视频面试",
        "time": "2026-07-08T14:00:00",
        "location": "https://meeting.example.com/abc123",
        "status": "scheduled",
        "notes": "候选人对产品经理职位有热情，重点考察产品思维和项目经验",
        "created_at": "2026-06-29T10:00:00",
        "updated_at": "2026-06-29T10:00:00"
    },
    {
        "id": "interview-002",
        "application_id": "app-001",
        "interviewer": "王芳",
        "round": "初试",
        "method": "现场面试",
        "time": "2026-07-06T10:00:00",
        "location": "北京市朝阳区建国路88号SOHO现代城A座18层",
        "status": "completed",
        "notes": "技术能力较强，沟通表达流畅，建议进入复试",
        "created_at": "2026-06-21T14:00:00",
        "updated_at": "2026-07-06T11:30:00"
    },
    {
        "id": "interview-003",
        "application_id": "app-001",
        "interviewer": "张伟",
        "round": "复试",
        "method": "视频面试",
        "time": "2026-07-10T15:00:00",
        "location": "https://meeting.example.com/xyz789",
        "status": "scheduled",
        "notes": "复试重点考察系统设计和团队协作能力",
        "created_at": "2026-07-06T14:00:00",
        "updated_at": "2026-07-06T14:00:00"
    },
    {
        "id": "interview-004",
        "application_id": "app-002",
        "interviewer": "刘洋",
        "round": "初试",
        "method": "电话面试",
        "time": "2026-07-07T11:00:00",
        "location": "13800138002",
        "status": "pending",
        "notes": "先进行电话沟通了解基本情况",
        "created_at": "2026-06-28T09:00:00",
        "updated_at": "2026-06-28T09:00:00"
    }
]

mock_offers = [
    {
        "id": "offer-001",
        "application_id": "app-001",
        "interview_id": "interview-002",
        "salary_min": 35000,
        "salary_max": 45000,
        "position_title": "高级前端工程师",
        "start_date": "2026-07-20T09:00:00",
        "notes": "13薪，年终奖视公司效益而定，入职后享有完善的培训体系",
        "status": "pending",
        "created_at": "2026-07-06T14:00:00",
        "updated_at": "2026-07-06T14:00:00"
    },
    {
        "id": "offer-002",
        "application_id": "app-003",
        "interview_id": None,
        "salary_min": 25000,
        "salary_max": 32000,
        "position_title": "产品经理",
        "start_date": "2026-07-15T09:00:00",
        "notes": "14薪，五险一金齐全，提供年度体检",
        "status": "accepted",
        "created_at": "2026-07-05T10:00:00",
        "updated_at": "2026-07-07T16:00:00"
    },
    {
        "id": "offer-003",
        "application_id": "app-004",
        "interview_id": None,
        "salary_min": 20000,
        "salary_max": 28000,
        "position_title": "UI设计师",
        "start_date": "2026-07-18T09:00:00",
        "notes": "13薪，弹性工作制",
        "status": "rejected",
        "created_at": "2026-07-04T11:00:00",
        "updated_at": "2026-07-06T09:00:00"
    }
]


@app.get("/api/stats", response_model=Stats)
def get_stats():
    total_jobs = len(mock_jobs)
    active_jobs = sum(1 for job in mock_jobs if job["status"] == "active")
    total_applications = len(mock_applications)
    pending_applications = sum(1 for app in mock_applications if app["status"] == "pending")
    communicating_applications = sum(1 for app in mock_applications if app["status"] == "communicating")
    interviewing_applications = sum(1 for app in mock_applications if app["status"] == "interviewing")
    hired_applications = sum(1 for app in mock_applications if app["status"] == "hired")
    rejected_applications = sum(1 for app in mock_applications if app["status"] == "rejected")
    total_interviews = len(mock_interviews)
    scheduled_interviews = sum(1 for i in mock_interviews if i["status"] == "scheduled")
    completed_interviews = sum(1 for i in mock_interviews if i["status"] == "completed")
    cancelled_interviews = sum(1 for i in mock_interviews if i["status"] == "cancelled")
    pending_interviews = sum(1 for i in mock_interviews if i["status"] == "pending")
    total_offers = len(mock_offers)
    pending_offers = sum(1 for o in mock_offers if o["status"] == "pending")
    accepted_offers = sum(1 for o in mock_offers if o["status"] == "accepted")
    rejected_offers = sum(1 for o in mock_offers if o["status"] == "rejected")
    withdrawn_offers = sum(1 for o in mock_offers if o["status"] == "withdrawn")
    pending_onboarding_offers = sum(1 for o in mock_offers if o["status"] == "pending_onboarding")
    return {
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "total_applications": total_applications,
        "pending_applications": pending_applications,
        "communicating_applications": communicating_applications,
        "interviewing_applications": interviewing_applications,
        "hired_applications": hired_applications,
        "rejected_applications": rejected_applications,
        "total_interviews": total_interviews,
        "scheduled_interviews": scheduled_interviews,
        "completed_interviews": completed_interviews,
        "cancelled_interviews": cancelled_interviews,
        "pending_interviews": pending_interviews,
        "total_offers": total_offers,
        "pending_offers": pending_offers,
        "accepted_offers": accepted_offers,
        "rejected_offers": rejected_offers,
        "withdrawn_offers": withdrawn_offers,
        "pending_onboarding_offers": pending_onboarding_offers
    }


@app.get("/api/jobs", response_model=List[Job])
def get_jobs(city: Optional[str] = None, status: Optional[str] = None, keyword: Optional[str] = None):
    result = mock_jobs.copy()
    if city:
        result = [job for job in result if job["city"] == city]
    if status:
        result = [job for job in result if job["status"] == status]
    if keyword:
        kw = keyword.lower()
        result = [job for job in result if kw in job["title"].lower() or kw in job["company"].lower()]
    return result


@app.get("/api/jobs/{job_id}", response_model=Job)
def get_job(job_id: str):
    job = next((job for job in mock_jobs if job["id"] == job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="职位不存在")
    return job


@app.post("/api/jobs", response_model=Job)
def create_job(job: dict):
    new_job = {
        "id": f"job-{len(mock_jobs) + 1:03d}",
        "title": job.get("title"),
        "company": job.get("company"),
        "city": job.get("city"),
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "experience": job.get("experience"),
        "education": job.get("education"),
        "tags": job.get("tags", []),
        "description": job.get("description"),
        "requirements": job.get("requirements"),
        "contact_email": job.get("contact_email"),
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    mock_jobs.append(new_job)
    return new_job


@app.put("/api/jobs/{job_id}", response_model=Job)
def update_job(job_id: str, job: dict):
    index = next((i for i, j in enumerate(mock_jobs) if j["id"] == job_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="职位不存在")
    mock_jobs[index].update(job)
    mock_jobs[index]["updated_at"] = datetime.now().isoformat()
    return mock_jobs[index]


@app.delete("/api/jobs/{job_id}")
def delete_job(job_id: str):
    index = next((i for i, j in enumerate(mock_jobs) if j["id"] == job_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="职位不存在")
    del mock_jobs[index]
    return {"message": "职位已删除"}


@app.get("/api/candidates", response_model=List[Candidate])
def get_candidates(
    desired_city: Optional[str] = None, 
    experience: Optional[str] = None, 
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    desired_job: Optional[str] = None
):
    result = mock_candidates.copy()
    if desired_city:
        result = [c for c in result if c["desired_city"] == desired_city]
    if experience:
        result = [c for c in result if experience in c["experience"]]
    if status:
        result = [c for c in result if c["status"] == status]
    if keyword:
        kw = keyword.lower()
        result = [c for c in result if 
                  kw in c["name"].lower() or 
                  kw in c["email"].lower() or
                  kw in c["desired_job"].lower() or
                  any(kw in skill.lower() for skill in c["skills"])]
    if desired_job:
        result = [c for c in result if desired_job.lower() in c["desired_job"].lower()]
    return result


@app.get("/api/candidates/{candidate_id}", response_model=Candidate)
def get_candidate(candidate_id: str):
    candidate = next((c for c in mock_candidates if c["id"] == candidate_id), None)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    return candidate


@app.post("/api/candidates", response_model=Candidate)
def create_candidate(candidate: dict):
    new_candidate = {
        "id": f"candidate-{len(mock_candidates) + 1:03d}",
        "name": candidate.get("name"),
        "email": candidate.get("email"),
        "phone": candidate.get("phone"),
        "education": candidate.get("education"),
        "experience": candidate.get("experience"),
        "resume": candidate.get("resume", ""),
        "skills": candidate.get("skills", []),
        "desired_job": candidate.get("desired_job", ""),
        "desired_city": candidate.get("desired_city", ""),
        "status": "active",
        "created_at": datetime.now().isoformat()
    }
    mock_candidates.append(new_candidate)
    return new_candidate


@app.get("/api/applications", response_model=List[Application])
def get_applications(job_id: Optional[str] = None, candidate_id: Optional[str] = None, status: Optional[str] = None):
    result = mock_applications.copy()
    if job_id:
        result = [app for app in result if app["job_id"] == job_id]
    if candidate_id:
        result = [app for app in result if app["candidate_id"] == candidate_id]
    if status:
        result = [app for app in result if app["status"] == status]
    return result


@app.get("/api/applications/{application_id}", response_model=Application)
def get_application(application_id: str):
    application = next((app for app in mock_applications if app["id"] == application_id), None)
    if not application:
        raise HTTPException(status_code=404, detail="投递记录不存在")
    return application


@app.post("/api/applications", response_model=Application)
def create_application(application: dict):
    job = next((j for j in mock_jobs if j["id"] == application["job_id"]), None)
    if not job:
        raise HTTPException(status_code=400, detail="职位不存在")
    new_application = {
        "id": f"app-{len(mock_applications) + 1:03d}",
        "job_id": application.get("job_id"),
        "candidate_id": application.get("candidate_id"),
        "status": "pending",
        "cover_letter": application.get("cover_letter", ""),
        "applied_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    mock_applications.append(new_application)
    return new_application


@app.put("/api/applications/{application_id}/status", response_model=Application)
def update_application_status(application_id: str, data: dict):
    index = next((i for i, app in enumerate(mock_applications) if app["id"] == application_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="投递记录不存在")
    new_status = data.get("status")
    if new_status not in ["pending", "communicating", "interviewing", "rejected", "hired"]:
        raise HTTPException(status_code=400, detail="无效的状态值")
    mock_applications[index]["status"] = new_status
    mock_applications[index]["updated_at"] = datetime.now().isoformat()
    return mock_applications[index]


@app.get("/api/messages", response_model=List[Message])
def get_messages(application_id: Optional[str] = None):
    if application_id:
        return [msg for msg in mock_messages if msg["application_id"] == application_id]
    return mock_messages


@app.post("/api/messages", response_model=Message)
def create_message(message: dict):
    application = next((app for app in mock_applications if app["id"] == message["application_id"]), None)
    if not application:
        raise HTTPException(status_code=400, detail="投递记录不存在")
    new_message = {
        "id": f"msg-{len(mock_messages) + 1:03d}",
        "application_id": message.get("application_id"),
        "sender_id": message.get("sender_id"),
        "sender_type": message.get("sender_type"),
        "content": message.get("content"),
        "sent_at": datetime.now().isoformat()
    }
    mock_messages.append(new_message)
    return new_message


@app.get("/api/cities")
def get_cities():
    cities = sorted(set(job["city"] for job in mock_jobs))
    return cities


@app.get("/api/statuses")
def get_statuses():
    return ["active", "closed"]


@app.get("/api/interviews", response_model=List[Interview])
def get_interviews(application_id: Optional[str] = None, candidate_id: Optional[str] = None, status: Optional[str] = None):
    result = mock_interviews.copy()
    if application_id:
        result = [i for i in result if i["application_id"] == application_id]
    if candidate_id:
        candidate_apps = [app["id"] for app in mock_applications if app["candidate_id"] == candidate_id]
        result = [i for i in result if i["application_id"] in candidate_apps]
    if status:
        result = [i for i in result if i["status"] == status]
    return result


@app.get("/api/interviews/{interview_id}", response_model=Interview)
def get_interview(interview_id: str):
    interview = next((i for i in mock_interviews if i["id"] == interview_id), None)
    if not interview:
        raise HTTPException(status_code=404, detail="面试记录不存在")
    return interview


@app.post("/api/interviews", response_model=Interview)
def create_interview(interview: dict):
    if not interview.get("application_id"):
        raise HTTPException(status_code=400, detail="请选择投递记录（application_id不能为空）")
    application = next((app for app in mock_applications if app["id"] == interview["application_id"]), None)
    if not application:
        raise HTTPException(status_code=400, detail="投递记录不存在")
    if not interview.get("time"):
        raise HTTPException(status_code=400, detail="请选择面试时间（time不能为空）")
    if not interview.get("method"):
        raise HTTPException(status_code=400, detail="请选择面试方式（method不能为空）")
    if not interview.get("interviewer"):
        raise HTTPException(status_code=400, detail="请输入面试官姓名（interviewer不能为空）")
    new_interview = {
        "id": f"interview-{len(mock_interviews) + 1:03d}",
        "application_id": interview["application_id"],
        "interviewer": interview["interviewer"],
        "round": interview.get("round", "初试"),
        "method": interview["method"],
        "time": interview["time"],
        "location": interview.get("location", ""),
        "status": interview.get("status", "pending"),
        "notes": interview.get("notes", ""),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    mock_interviews.append(new_interview)
    return new_interview


@app.put("/api/interviews/{interview_id}", response_model=Interview)
def update_interview(interview_id: str, data: dict):
    index = next((i for i, interview in enumerate(mock_interviews) if interview["id"] == interview_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="面试记录不存在")
    mock_interviews[index].update(data)
    mock_interviews[index]["updated_at"] = datetime.now().isoformat()
    return mock_interviews[index]


@app.put("/api/interviews/{interview_id}/status", response_model=Interview)
def update_interview_status(interview_id: str, data: dict):
    index = next((i for i, interview in enumerate(mock_interviews) if interview["id"] == interview_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="面试记录不存在")
    new_status = data.get("status")
    if new_status not in ["pending", "scheduled", "completed", "cancelled"]:
        raise HTTPException(status_code=400, detail="无效的状态值")
    mock_interviews[index]["status"] = new_status
    mock_interviews[index]["updated_at"] = datetime.now().isoformat()
    return mock_interviews[index]


@app.get("/api/offers", response_model=List[Offer])
def get_offers(status: Optional[str] = None, application_id: Optional[str] = None, candidate_id: Optional[str] = None, keyword: Optional[str] = None, job_id: Optional[str] = None):
    result = mock_offers.copy()
    if status:
        result = [o for o in result if o["status"] == status]
    if application_id:
        result = [o for o in result if o["application_id"] == application_id]
    if candidate_id:
        candidate_apps = [app["id"] for app in mock_applications if app["candidate_id"] == candidate_id]
        result = [o for o in result if o["application_id"] in candidate_apps]
    if job_id:
        job_apps = [app["id"] for app in mock_applications if app["job_id"] == job_id]
        result = [o for o in result if o["application_id"] in job_apps]
    if keyword:
        kw = keyword.lower()
        matched_ids = set()
        for o in result:
            app = next((a for a in mock_applications if a["id"] == o["application_id"]), None)
            if app:
                candidate = next((c for c in mock_candidates if c["id"] == app["candidate_id"]), None)
                job = next((j for j in mock_jobs if j["id"] == app["job_id"]), None)
                if (candidate and kw in candidate["name"].lower()) or \
                   (job and kw in job["title"].lower()) or \
                   kw in o["position_title"].lower():
                    matched_ids.add(o["id"])
        result = [o for o in result if o["id"] in matched_ids]
    return result


@app.get("/api/offers/{offer_id}", response_model=Offer)
def get_offer(offer_id: str):
    offer = next((o for o in mock_offers if o["id"] == offer_id), None)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer记录不存在")
    return offer


@app.get("/api/offers/{offer_id}/details")
def get_offer_details(offer_id: str):
    offer = next((o for o in mock_offers if o["id"] == offer_id), None)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer记录不存在")

    result = {
        "offer": offer,
        "application": None,
        "job": None,
        "candidate": None,
        "interviews": [],
        "latest_interview": None
    }

    app_id = offer.get("application_id")
    if app_id:
        application = next((a for a in mock_applications if a["id"] == app_id), None)
        if application:
            result["application"] = application

            job = next((j for j in mock_jobs if j["id"] == application["job_id"]), None)
            if job:
                result["job"] = job

            candidate = next((c for c in mock_candidates if c["id"] == application["candidate_id"]), None)
            if candidate:
                result["candidate"] = candidate

            interviews = [i for i in mock_interviews if i["application_id"] == app_id]
            result["interviews"] = interviews
            if interviews:
                result["latest_interview"] = max(interviews, key=lambda x: x["time"])

    return result


@app.post("/api/offers", response_model=Offer)
def create_offer(offer: dict):
    if not offer.get("application_id"):
        raise HTTPException(status_code=400, detail="请选择投递记录（application_id不能为空）")
    application = next((app for app in mock_applications if app["id"] == offer["application_id"]), None)
    if not application:
        raise HTTPException(status_code=400, detail="投递记录不存在")
    if not offer.get("salary_min") or not offer.get("salary_max"):
        raise HTTPException(status_code=400, detail="请输入薪资范围（salary_min和salary_max不能为空）")
    if offer.get("salary_min") >= offer.get("salary_max"):
        raise HTTPException(status_code=400, detail="薪资下限不能大于等于上限")
    if not offer.get("position_title"):
        raise HTTPException(status_code=400, detail="请输入职位名称（position_title不能为空）")
    if not offer.get("start_date"):
        raise HTTPException(status_code=400, detail="请选择入职时间（start_date不能为空）")
    
    new_offer = {
        "id": f"offer-{len(mock_offers) + 1:03d}",
        "application_id": offer["application_id"],
        "interview_id": offer.get("interview_id"),
        "salary_min": offer["salary_min"],
        "salary_max": offer["salary_max"],
        "position_title": offer["position_title"],
        "start_date": offer["start_date"],
        "notes": offer.get("notes", ""),
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    mock_offers.append(new_offer)
    return new_offer


@app.put("/api/offers/{offer_id}", response_model=Offer)
def update_offer(offer_id: str, data: dict):
    index = next((i for i, offer in enumerate(mock_offers) if offer["id"] == offer_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Offer记录不存在")
    
    if "salary_min" in data and "salary_max" in data:
        if data["salary_min"] >= data["salary_max"]:
            raise HTTPException(status_code=400, detail="薪资下限不能大于等于上限")
    
    mock_offers[index].update(data)
    mock_offers[index]["updated_at"] = datetime.now().isoformat()
    return mock_offers[index]


@app.put("/api/offers/{offer_id}/status", response_model=Offer)
def update_offer_status(offer_id: str, data: dict):
    index = next((i for i, offer in enumerate(mock_offers) if offer["id"] == offer_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Offer记录不存在")
    
    new_status = data.get("status")
    valid_statuses = ["pending", "accepted", "rejected", "withdrawn", "pending_onboarding"]
    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"无效的状态值，可选值：{', '.join(valid_statuses)}")
    
    old_status = mock_offers[index]["status"]
    mock_offers[index]["status"] = new_status
    mock_offers[index]["updated_at"] = datetime.now().isoformat()
    
    app_id = mock_offers[index]["application_id"]
    app_index = next((i for i, app in enumerate(mock_applications) if app["id"] == app_id), None)
    if app_index is not None:
        if new_status == "accepted":
            mock_applications[app_index]["status"] = "hired"
        elif new_status == "rejected":
            mock_applications[app_index]["status"] = "rejected"
        elif new_status == "pending_onboarding":
            mock_applications[app_index]["status"] = "hired"
        elif new_status == "pending":
            if mock_applications[app_index]["status"] in ["hired", "rejected"]:
                mock_applications[app_index]["status"] = "interviewing"
        elif new_status == "withdrawn":
            if mock_applications[app_index]["status"] == "hired":
                mock_applications[app_index]["status"] = "interviewing"
        mock_applications[app_index]["updated_at"] = datetime.now().isoformat()
    
    return mock_offers[index]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)