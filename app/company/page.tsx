import Link from "next/link"
import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Building2, Search, Filter, MessageSquare, Star, Bookmark } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export default function CompanyPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-xl">
            <Building2 className="h-6 w-6" />
            <Link href="/">TalentConnect</Link>
          </div>
          <nav className="flex items-center gap-6">
            <Link href="/company/dashboard" className="text-sm font-medium hover:underline">
              대시보드
            </Link>
            <Link href="/company/messages" className="text-sm font-medium hover:underline">
              메시지
            </Link>
            <Link href="/company/saved" className="text-sm font-medium hover:underline">
              저장된 인재
            </Link>
            <div className="h-8 w-8 rounded-full bg-muted overflow-hidden">
              <Image
                src="/placeholder.svg?height=32&width=32"
                alt="Company"
                width={32}
                height={32}
                className="h-full w-full object-cover"
              />
            </div>
          </nav>
        </div>
      </header>
      <main className="flex-1">
        <div className="container py-8">
          <div className="mb-8 space-y-4">
            <h1 className="text-3xl font-bold">인재 탐색</h1>
            <p className="text-muted-foreground">
              KDT 부트캠프 수료생들의 포트폴리오를 확인하고 최적의 인재를 찾아보세요.
            </p>
            <div className="flex flex-col gap-4 sm:flex-row">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input placeholder="이름, 기술 스택, 직무 등으로 검색" className="pl-10" />
              </div>
              <Select>
                <SelectTrigger className="w-full sm:w-[180px]">
                  <SelectValue placeholder="직군 선택" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="frontend">프론트엔드</SelectItem>
                  <SelectItem value="backend">백엔드</SelectItem>
                  <SelectItem value="fullstack">풀스택</SelectItem>
                  <SelectItem value="mobile">모바일</SelectItem>
                  <SelectItem value="design">UI/UX 디자인</SelectItem>
                </SelectContent>
              </Select>
              <Button variant="outline" className="gap-2">
                <Filter className="h-4 w-4" />
                필터
              </Button>
            </div>
          </div>

          <Tabs defaultValue="all">
            <TabsList className="mb-6">
              <TabsTrigger value="all">전체</TabsTrigger>
              <TabsTrigger value="frontend">프론트엔드</TabsTrigger>
              <TabsTrigger value="backend">백엔드</TabsTrigger>
              <TabsTrigger value="fullstack">풀스택</TabsTrigger>
              <TabsTrigger value="mobile">모바일</TabsTrigger>
              <TabsTrigger value="design">UI/UX 디자인</TabsTrigger>
            </TabsList>

            <TabsContent value="all" className="space-y-6">
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {[1, 2, 3, 4, 5, 6].map((candidate) => (
                  <Card key={candidate} className="overflow-hidden">
                    <CardHeader className="p-0">
                      <div className="h-32 bg-gradient-to-r from-primary/20 to-primary/10"></div>
                    </CardHeader>
                    <CardContent className="p-6 pt-0">
                      <div className="flex justify-between -mt-10">
                        <div className="h-20 w-20 rounded-full border-4 border-background bg-muted overflow-hidden">
                          <Image
                            src={`/placeholder.svg?height=80&width=80&text=User+${candidate}`}
                            alt={`Candidate ${candidate}`}
                            width={80}
                            height={80}
                            className="h-full w-full object-cover"
                          />
                        </div>
                        <div className="flex gap-1 pt-2">
                          <Button variant="ghost" size="icon" className="h-8 w-8">
                            <Bookmark className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="icon" className="h-8 w-8">
                            <Star className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                      <div className="mt-3 space-y-3">
                        <div>
                          <h3 className="font-medium">홍길동 {candidate}</h3>
                          <p className="text-sm text-muted-foreground">
                            {candidate % 3 === 0
                              ? "프론트엔드 개발자"
                              : candidate % 3 === 1
                                ? "백엔드 개발자"
                                : "풀스택 개발자"}
                          </p>
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {candidate % 3 === 0 ? (
                            <>
                              <Badge variant="outline">React</Badge>
                              <Badge variant="outline">TypeScript</Badge>
                              <Badge variant="outline">Next.js</Badge>
                            </>
                          ) : candidate % 3 === 1 ? (
                            <>
                              <Badge variant="outline">Node.js</Badge>
                              <Badge variant="outline">Express</Badge>
                              <Badge variant="outline">MongoDB</Badge>
                            </>
                          ) : (
                            <>
                              <Badge variant="outline">React</Badge>
                              <Badge variant="outline">Node.js</Badge>
                              <Badge variant="outline">AWS</Badge>
                            </>
                          )}
                        </div>
                        <p className="text-sm">
                          {candidate % 3 === 0
                            ? "사용자 경험을 중시하는 프론트엔드 개발자입니다. 반응형 웹 디자인과 성능 최적화에 관심이 많습니다."
                            : candidate % 3 === 1
                              ? "안정적인 서버 구축과 데이터베이스 설계에 강점이 있는 백엔드 개발자입니다."
                              : "프론트엔드와 백엔드 모두 다룰 수 있는 풀스택 개발자입니다. 전체 개발 프로세스를 이해하고 있습니다."}
                        </p>
                      </div>
                    </CardContent>
                    <CardFooter className="flex justify-between border-t p-4">
                      <div className="text-sm text-muted-foreground">
                        KDT 부트캠프 {candidate % 2 === 0 ? "5기" : "6기"} 수료
                      </div>
                      <Button size="sm" className="gap-1">
                        <MessageSquare className="h-4 w-4" />
                        연락하기
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
              </div>
              <div className="flex justify-center">
                <Button variant="outline">더 보기</Button>
              </div>
            </TabsContent>

            {["frontend", "backend", "fullstack", "mobile", "design"].map((tab) => (
              <TabsContent key={tab} value={tab}>
                <div className="rounded-lg border bg-card p-8 text-center">
                  <h3 className="text-lg font-medium mb-2">
                    {tab === "frontend"
                      ? "프론트엔드"
                      : tab === "backend"
                        ? "백엔드"
                        : tab === "fullstack"
                          ? "풀스택"
                          : tab === "mobile"
                            ? "모바일"
                            : "UI/UX 디자인"}{" "}
                    개발자
                  </h3>
                  <p className="text-muted-foreground mb-4">이 카테고리의 인재들을 보려면 필터를 적용하세요.</p>
                  <Button>필터 적용하기</Button>
                </div>
              </TabsContent>
            ))}
          </Tabs>
        </div>
      </main>
      <footer className="border-t py-6">
        <div className="container flex flex-col items-center justify-center gap-4 text-center">
          <p className="text-sm text-muted-foreground">© 2025 TalentConnect. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
