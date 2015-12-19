set(LLVM_LINK_COMPONENTS support)
set(LLVM_USED_LIBS clangTooling clangBasic clangAST)

add_clang_executable(test-check
  TestCheck.cpp
  )

target_link_libraries(test-check
  clangTooling
  clangBasic
  clangASTMatchers
  )

set_target_properties(test-check PROPERTIES
  OUTPUT_NAME test-check
  )
